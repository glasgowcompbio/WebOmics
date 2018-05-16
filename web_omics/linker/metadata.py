from bioservices.kegg import KEGG
from bioservices import Ensembl
from bioservices import UniProt
import json
import urllib.request
import pickle


################################################################################
### Gene-related functions                                                   ###
################################################################################


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def get_ensembl_metadata_online(ensembl_ids):

    ensembl_ids = list(set(ensembl_ids))
    print('get_ensembl_metadata', len(ensembl_ids))

    BATCH_SIZE = 1000
    ens = Ensembl()
    ensembl_lookup = {}
    cumulative_total = 0
    for x in batch(ensembl_ids, BATCH_SIZE):
        batch_ids = [i for i in x]
        cumulative_total += len(batch_ids)
        print(cumulative_total, '/', len(ensembl_ids))
        lookup = ens.post_lookup_by_id(identifiers=batch_ids)
        ensembl_lookup.update(lookup)

    return ensembl_lookup


def get_single_ensembl_metadata_online(ensembl_id):
    ens = Ensembl()
    res = ens.get_lookup_by_id(ensembl_id, expand=True)
    return res


def get_gene_names(ensembl_ids, pickled_gene_names_url):
    metadata_map = {}
    with urllib.request.urlopen(pickled_gene_names_url) as url:
        gtf_dict = pickle.load(url)
        for ensembl_id in ensembl_ids:
            try:
                display_name = gtf_dict[ensembl_id]
                display_name = clean_label(display_name)
                metadata_map[ensembl_id] = {'display_name': display_name}
            except KeyError:
                metadata_map[ensembl_id] = {'display_name': ensembl_id}
    return metadata_map


################################################################################
### Protein-related functions                                                ###
################################################################################


def get_uniprot_metadata_online(uniprot_ids):

    uniprot_ids = list(set(uniprot_ids))
    print('get_uniprot_metadata', len(uniprot_ids))

    BATCH_SIZE = 200
    uniprot = UniProt()
    uniprot_lookup = {}

    cumulative_total = 0
    for x in batch(uniprot_ids, BATCH_SIZE):
        batch_ids = [i for i in x]
        cumulative_total += len(batch_ids)
        print(cumulative_total, '/', len(uniprot_ids))

        res = uniprot.retrieve(batch_ids)
        for r in res:
            for key in r['accession']:
                protein_id = key.contents[0]
                for x in r['recommendedname']:
                    tag = x.find('shortname')
                    if tag is None:
                        tag = x.find('fullname')
                    label = tag.contents[0]
                    uniprot_lookup[protein_id] = {'display_name': label}

    return uniprot_lookup


def get_single_uniprot_metadata_online(uniprot_id):
    uniprot = UniProt()
    res = uniprot.retrieve(uniprot_id)
    return res


def clean_label(w):
    results = []
    for tok in w.split(' '):
        # filtered = re.sub(r'[^\w\s]', '', tok)
        filtered = tok.replace("'", "")
        results.append(filtered.strip())
    return ' '.join(results)


def get_uniprot_metadata_reactome(uniprot_ids):
    protein_descriptions = {}  # TODO: get the description of each protein from reactome
    metadata_map = {}
    for protein_id in protein_descriptions:
        metadata_map[protein_id] = {'display_name': protein_id}
        if protein_id in protein_descriptions and protein_descriptions[protein_id] is not None:
            desc = protein_descriptions[protein_id]
            tokens = desc.split(':')
            for i in range(len(tokens)):
                w = tokens[i]
                if w.startswith('recommendedName'):
                    next_w = clean_label(tokens[i + 1])
                    metadata_map[protein_id] = {'display_name': next_w}
                    print(protein_id, '--', next_w)
    return metadata_map


################################################################################
### Compound-related functions                                               ###
################################################################################

def get_compound_metadata_online(kegg_ids):

    s = KEGG()
    metadata_map = {}
    for i in range(len(kegg_ids)):
        try:
            if i % 10 == 0:
                print("Retrieving %d/%d KEGG records" % (i, len(kegg_ids)))
            kegg_id = kegg_ids[i]
            res = s.get(kegg_id)
            d = s.parse(res)
            first_name = d['NAME'][0]
            first_name = first_name.replace(';', '') # strip last ';' character
            metadata_map[kegg_id] = {'display_name': first_name}
        except TypeError:
            print('kegg_id=%s parsed_data=%s' % (kegg_id, d))
    return metadata_map


def get_compound_metadata_from_json(compound_ids, json_url):
    metadata_map = {}
    with urllib.request.urlopen(json_url) as url:
        lookup = json.loads(url.read().decode())
        for compound_id in compound_ids:
            try:
                display_name = clean_label(lookup[compound_id]['display_name'])
                metadata_map[compound_id] = {'display_name': display_name}
            except KeyError:
                metadata_map[compound_id] = {'display_name': compound_id}
    return metadata_map


def get_single_compound_metadata_online(kegg_id):

    s = KEGG()
    res = s.get(kegg_id)
    d = s.parse(res)
    return d

################################################################################
### Reaction-related functions                                               ###
################################################################################


################################################################################
### Pathway-related functions                                                ###
################################################################################
