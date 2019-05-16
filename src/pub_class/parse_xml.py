import pandas as pd
import xml.etree.ElementTree as ET
import io

# etree = ET.parse("desc2019.xml")
# dfcols = ['concept', 'desc']
# df = pd.DataFrame(columns=dfcols)
#
# for conceptList in etree.iter(tag = 'ConceptList'):
#     for concept in conceptList.iter(tag = 'Concept'):
#
#         if concept.get('PreferredConceptYN') == 'Y':
#             conceptname = concept.iter(tag = "ConceptName")
#             name = ""
#             for cname in conceptname:
#                 name = cname.find("String").text
#             # print(name)
#             try:
#                 descrip = concept.find("ScopeNote").text
#             except:
#                 descrip = None
#
#             if descrip is not None:
#                 # print(name)
#                 df = df.append(
#                     {'concept' : name,
#                      'desc': descrip}
#                     , ignore_index=True)

files = ['pubmed19n0055.xml']


dfcols = ['abstract', 'mesh']
df = pd.DataFrame(columns=dfcols)

for file in files:
    etree = ET.parse(file)
    for articleSet in etree.iter(tag='PubmedArticleSet'):
        for pubarticle in articleSet.iter(tag='PubmedArticle'):
            abstract = None
            for article in pubarticle.iter(tag='Article'):

                try:
                    temp = article.find("Abstract")
                    abstract = temp.find("AbstractText").text
                except:
                    abstract = None

            if abstract is not None:
                for headinglist in pubarticle.iter(tag='MeshHeadingList'):
                    for heading in headinglist.iter(tag='MeshHeading'):
                        if heading.find("DescriptorName").get("MajorTopicYN") == 'Y':
                            mesh = heading.find("DescriptorName").text

                            df = df.append(
                                {'abstract': abstract,
                                'mesh': mesh}
                                , ignore_index=True)


data2 = df[df['mesh'].isin(['Epitopes', 'Immunity, Cellular', 'Staining and Labeling', 'Antibody Formation', 'Genes',
                               'Hydrogen-Ion Concentration', 'Histocompatibility Antigens', 'Electroencephalography',
                               'Antigens', 'HLA Antigens', 'Aging'])]

data = df[df['abstract'].isin(data2['abstract'].tolist())]

print(data2.head())
print(len(data2))
print(len(data))


# df.to_csv('test.csv')
