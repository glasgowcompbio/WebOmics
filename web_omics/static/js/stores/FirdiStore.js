import Observable from './Observable';
import {GROUP_LOADED_EVENT, LAST_CLICKED_FIRDI, LAST_CLICKED_GROUP_MANAGER, SELECTION_UPDATE_EVENT} from "../common";
import {getConstraintTablesConstraintKeyName, getDisplayName, isTableVisible} from "../firdi/Utils";
import {action, autorun, computed, observable} from 'mobx';
import SqlManager from "../firdi/SqlManager";


class FirdiStore extends Observable {

    // public fields
    tablesInfo = undefined;
    tableFields = undefined;
    defaultConstraints = undefined;
    dataTablesIds = undefined;
    fieldNames = undefined;
    displayNameToConstraintKey = undefined;

    // private stuff
    tableIdToIdColumnMap = undefined;
    lastQueryResult = null;

    // reactive stuff
    @observable selections = undefined;
    @observable whereType = null;
    @observable selectedIndex = {};

    constructor(rootStore, tablesInfo, tableFields) {
        super();
        this.rootStore = rootStore;
        this.tablesInfo = tablesInfo;
        this.tableFields = tableFields;

        // precompute stuff that won't change
        this.defaultConstraints = this.getDefaultConstraints();
        this.dataTablesIds = this.getDataTablesIds();
        this.fieldNames = this.getFieldNames();
        this.displayNameToConstraintKey = this.getDisplayNameToConstraintKey();
        this.tableIdToIdColumnMap = this.getTableIdToIdColumnMap();

        this.selections = this.emptySelections();
        this.sqlManager = new SqlManager(this.tablesInfo);

        autorun(() => {
            // set original cgm nodes
            let originalCgmNodes = undefined;
            if (this.rootStore.cgmStore) { // undefined when RootStore is still initialising
                originalCgmNodes = this.rootStore.cgmStore.originalCgmNodes;
            }

            // create data that will be sent to the observers
            this.lastQueryResult = this.queryResult;
            const data = {
                'totalSelected': this.totalSelected,
                'selections': this.selections,
                'queryResult': this.lastQueryResult,
                'originalCgmNodes': originalCgmNodes,
                'whereType': this.whereType
            }
            console.log('%c FirdiStore autorun ', 'background: #222; color: #bada55', data);
            this.notifyUpdate(data);
        });
    }

    // mobx computer properties

    @computed get numSelected() {
        return this.countNumSelected();
    }

    @computed get totalSelected() {
        const values = Object.values(this.numSelected);
        const total = values.reduce((a, b) => a + b, 0);
        return total;
    }

    @computed get constraints() {
        return this.makeConstraints();
    }

    @computed get queryResult() {
        // console.trace('queryResult');

        // get alasql query result
        const resultset = this.sqlManager.queryDatabase(this.tablesInfo, this.constraints,
            this.whereType);

        // get results for each table
        const fieldNames = this.fieldNames;
        const tableData = {};
        for (let i = 0; i < fieldNames.length; i++) {
            const tableFieldNames = fieldNames[i];
            const tableName = tableFieldNames['tableName'];
            const data = this.sqlManager.prefixQuery(tableFieldNames, resultset);
            tableData[tableName] = data;
        }

        return tableData;
    }

    // mobx actions

    @action.bound
    addConstraint(tableName, rowData, rowIndex) {
        const idVal = this.getId(tableName, rowData);
        const displayName = getDisplayName(rowData, tableName);
        this.selections[tableName].push({
            idVal: idVal,
            rowIndex: rowIndex,
            displayName: displayName
        });

        // ensure that entries are sorted by rowIndex asc
        // this.selections[tableName].sort((a, b) => a.rowIndex - b.rowIndex);

        // same as above, but using a special syntax for mobx
        const observableArray = this.selections[tableName];
        observableArray.replace(observableArray.slice().sort((a, b) => a.rowIndex - b.rowIndex));
    }

    @action.bound
    removeConstraint(tableName, rowData) {
        const idVal = this.getId(tableName, rowData);
        this.selections[tableName] = this.selections[tableName].filter(x => x.idVal !== idVal);
    }

    @action.bound
    restoreSelection(newState) {
        this.selections = newState.selections;
        this.whereType = newState.whereType;
        this.lastQueryResult = null;
    }

    @action.bound
    reset() {
        this.selections = this.emptySelections();
        this.whereType = null;
        this.lastQueryResult = null;
    }

    @action.bound
    setWhereType(newType) {
        this.whereType = newType;
    }

    notifyUpdate(data) {
        if (this.rootStore.lastClicked == LAST_CLICKED_FIRDI) {
            this.fire(SELECTION_UPDATE_EVENT, data);
        } else if (this.rootStore.lastClicked == LAST_CLICKED_GROUP_MANAGER) {
            this.fire(GROUP_LOADED_EVENT, data);
        }
    }

    // TODO: should be made private methods

    getDefaultConstraints() {
        return getConstraintTablesConstraintKeyName(this.tablesInfo)
            .reduce((constraints, tableInfo) => {
                constraints[tableInfo['tableName']] = this.getKeys(
                    this.tablesInfo, tableInfo['tableName'], tableInfo['constraintKeyName']);
                return constraints;
            }, {});
    }

    getDataTablesIds() {
        return this.tablesInfo.filter(isTableVisible).reduce((apis, t) => {
            apis[t['tableName']] = "#" + t['tableName'];
            return apis
        }, {});
    }

    getFieldNames() {
        // Gets the field names for each visible table
        return this.tablesInfo
            .filter(isTableVisible)
            .map(tableInfo => ({
                'tableName': tableInfo['tableName'],
                'fieldNames': Object.keys(tableInfo['tableData'][0])
            }));
    }

    getDisplayNameToConstraintKey() {
        return getConstraintTablesConstraintKeyName(this.tablesInfo)
            .reduce((constraints, tableInfo) => {
                constraints[tableInfo['tableName']] = this.getDisplayNameToPk(
                    this.tablesInfo, tableInfo['tableName'], tableInfo['constraintKeyName']);
                return constraints;
            }, {});
    }

    getTableIdToIdColumnMap() {
        // Get the table name and key used in the WHERE clause in the form tableName: key
        return getConstraintTablesConstraintKeyName(this.tablesInfo)
            .map(t => ({[t['tableName']]: t['constraintKeyName']}))
            .reduce((o, v) => Object.assign(o, v), {});
    }

    getKeys(tablesInfo, tableName, k) {
        // Gets the values of the key used in the table relationship for the SQL IN clause
        const data = tablesInfo
            .filter(isTableVisible)
            .filter(t => t['tableName'] === tableName)
            .map(t => t['tableData'])[0];

        const keys = data
            .map(d => d[k])
            .filter((k, idx, arr) => arr.indexOf(k) === idx);

        return keys;
    }

    getDisplayNameToPk(tablesInfo, tableName, k) {
        // Gets the values of the key used in the table relationship for the SQL IN clause
        const data = tablesInfo
            .filter(isTableVisible)
            .filter(t => t['tableName'] === tableName)
            .map(t => t['tableData'])[0];

        const displayNameToPk = {}
        data.map(d => {
            const displayName = getDisplayName(d, tableName);
            displayNameToPk[displayName] = d[k];
        })
        return displayNameToPk;
    }

    getId(tableName, rowObject) {
        const idColumn = this.tableIdToIdColumnMap[tableName];
        return rowObject[idColumn];
    }

    countNumSelected() {
        return getConstraintTablesConstraintKeyName(this.tablesInfo)
            .reduce((results, tableInfo) => {
                const tname = tableInfo['tableName'];
                results[tname] = this.selections[tname].length;
                return results;
            }, {});
    }

    emptySelections() {
        return getConstraintTablesConstraintKeyName(this.tablesInfo)
            .reduce((results, tableInfo) => {
                const tname = tableInfo['tableName'];
                results[tname] = [];
                return results;
            }, {});
    }

    makeConstraints() {
        return getConstraintTablesConstraintKeyName(this.tablesInfo)
            .reduce((results, tableInfo) => {
                const tname = tableInfo['tableName'];
                results[tname] = this.selectionToConstraint(tname);
                return results;
            }, {});
    }

    selectionToConstraint(tableName) {
        if (this.numSelected[tableName] == 0) {
            return this.defaultConstraints[tableName];
        } else {
            return this.selections[tableName].map(x => x.idVal);
        }
    }

}

export default FirdiStore;