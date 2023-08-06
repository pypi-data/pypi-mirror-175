import pandas as pd
import urllib


def load_entities(path, lang, site):
    per_classes = ['subject', 'fictional-character', 'fictional-person']

    loc_classes = ['geographic-entity', 'fictional-location']

    org_classes = ['armed-organization', 'association', 'business', 'fictional-organisation',
                   'group-of-people', 'institution', 'organ']

    woa = pd.read_pickle("{}/{}-work-of-arts.pkl".format(path, lang))

    def load_classes(cl, entity_type):
        files = ['{}/{}-{}.pkl'.format(path, lang, c) for c in cl]

        tmp = pd.concat([pd.read_pickle(f) for f in files], sort=True).\
            drop_duplicates(subset=[entity_type]).\
            reset_index(drop=True)

        tmp = tmp.loc[~tmp[entity_type].isin(woa.woa)]. \
            reset_index(drop=True). \
            rename(columns={entity_type: 'wikidata'})

        return tmp

    per = load_classes(per_classes, 'person')

    loc = load_classes(loc_classes, 'location')

    org = load_classes(org_classes, 'organisation')

    ent = pd.concat([per, loc, org], sort=True)

    ent['dateofbirth'] = pd.to_datetime(ent.dateofbirth, yearfirst=True, errors="coerce")
    ent['inception'] = pd.to_datetime(ent.inception, yearfirst=True, errors="coerce")

    ent = ent.groupby('wikidata', as_index=False).first()

    coords = ent.coords.str.extract(r'Point\(([\-0-9E.]+)\W.([\-0-9E.]+)\)'). \
        rename(columns={0: "longitude", 1: "latitude"})

    ent['longitude'] = coords.longitude
    ent['latitude'] = coords.latitude

    # ent = ent.drop(columns=['coords'])

    ent = ent.sort_values(['dateofbirth', 'inception'], ascending=[True, True])

    ent = ent.drop_duplicates(subset=['wikidata'], keep="first"). \
        reset_index(drop=True). \
        set_index('wikidata')

    ent['PER'] = False
    ent['LOC'] = False
    ent['ORG'] = False

    ent.loc[per.wikidata, 'PER'] = True
    ent.loc[loc.wikidata, 'LOC'] = True
    ent.loc[org.wikidata, 'ORG'] = True

    ent['page_title'] = [urllib.parse.unquote(s) for s in ent.sitelink.str.replace(site, '').to_list()]

    ent = ent.reset_index().set_index('page_title')

    ent.loc[ent.PER & ent.ORG, 'PER'] = False

    ent['TYPE'] = [(('PER|' if p else "|") + ('LOC|' if l else "|") + ('ORG' if o else "")).strip('|')
                   for p, l, o in zip(ent.PER.to_list(), ent.LOC.to_list(), ent.ORG.to_list())]

    ent = ent.loc[~ent.index.duplicated()].sort_index()

    ent['QID'] = ent.wikidata.str.extract(r'.*?(Q[0-9]+).*?')

    ent = ent.loc[~ent.index.duplicated()].sort_index()

    ent['QID'] = ent.wikidata.str.extract(r'.*?(Q[0-9]+).*?')

    return ent
