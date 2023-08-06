from io import open
from setuptools import find_packages, setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name="qurator-sbb-tools",
    version="0.0.1",
    author="The Qurator Team",
    author_email="qurator@sbb.spk-berlin.de",
    description="Qurator",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    keywords='qurator',
    license='Apache',
    url="https://qurator.ai",
    packages=find_packages(exclude=["*.tests", "*.tests.*",
                                    "tests.*", "tests"]),
    install_requires=install_requires,
    entry_points={
      'console_scripts': [
        "altotool=qurator.sbb.xml:altotool",
        "alto-annotator=qurator.sbb.xml:altoannotator",
        "corpusentropy=qurator.sbb.entropy:main",
        "corpuslanguage=qurator.sbb.language:main",
        "select-by-lang-and-entropy=qurator.sbb.select:by_lang_and_entropy",
        "select-by-lang=qurator.sbb.select:by_lang",

        "collectcorpus=qurator.bert.corpus:collect",
        "bert-pregenerate-trainingdata=qurator.bert.pregenerate_training_data:main",
        "bert-finetune=qurator.bert.finetune_on_pregenerated:main",

        "extract-wiki-full-text-parquet=qurator.wikipedia.xml:to_parquet",
        "extract-wiki-full-text-sqlite=qurator.wikipedia.xml:to_sqlite",
        "extract-wiki-ner-entities=qurator.wikipedia.entities:extract",
        "wikidatamapping=qurator.wikipedia.entities:wikidatamapping",
        "redirects2entities=qurator.wikipedia.entities:redirects2entities",
        "redirects2pkl=qurator.wikipedia.entities:redirects2pkl",
        "compute-apriori-probs=qurator.wikipedia.entities:compute_apriori_probs",
        "tag-wiki-entities2parquet=qurator.wikipedia.ner:tag_entities2parquet",
        "tag-wiki-entities2sqlite=qurator.wikipedia.ner:tag_entities2sqlite",
        "print-wiki-article=qurator.wikipedia.ner:print_article_command_line",
        "train-test-split-wiki=qurator.wikipedia.ner:train_test_split",

        "find-entities=qurator.utils.entities:find_entities",
        "parquet2csv=qurator.utils.parquet:to_csv",
        "csv2sqlite=qurator.utils.csv:to_sqlite",
        "df2sqlite=qurator.utils.pickle:to_sqlite",
        "batchner=qurator.sbb.ner:on_db_file",
        "ned-statistics=qurator.sbb.ned:ned_statistics",
        "show-ner-models=qurator.sbb.ner:show_models",

        "example=qurator.examples.multiprocessing:example",

        "run-sparql=qurator.wikidata.cli:cli_run_sparql",
        "join-entities=qurator.wikidata.cli:join_entities",
        "batchel=qurator.sbb.ned:run_on_corpus",
        "batchel-wp=qurator.wikipedia.ned:run_on_tagged",

        "extract-corpus=qurator.topic_modeling.cli:extract_corpus",
        "extract-docs=qurator.topic_modeling.cli:extract_docs",
        "lda-grid-search=qurator.topic_modeling.cli:lda_grid_search",
        "run-lda=qurator.topic_modeling.cli:run_lda",
        "make-topicm-config=qurator.topic_modeling.cli:make_config"
      ]
    },
    python_requires='>=3.6.0',
    tests_require=['pytest'],
    classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
