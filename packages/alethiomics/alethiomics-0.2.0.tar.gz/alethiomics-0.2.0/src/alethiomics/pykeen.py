"""Modules used for working with Knowledge Graphs using pykeen framework.
"""
# imports
from pandas import DataFrame, concat
from pykeen.pipeline import pipeline as pykeen_pipeline
from pykeen.models import predict
from pandas import read_csv

def names2id(names, id_table):
    """Convert common names (genes, diseases etc.) to IDs.

    Parameters
    ----------
    names: list
        List of common names.
    id_table: pandas DataFrame
        A pandas DataFrame with two columns: 'id' and 'name'

    Returns
    -------
    ids: list
        List of IDs.
    """

    ids = id_table.loc[id_table['name'].isin(names), 'id'].tolist()

    return(ids)

def id2names(predictions, id_table_head, id_table_tail):
    """Convert IDs in the pykeen prediction DataFrame to common names.

    Parameters
    ----------
    predictions: pandas DataFrame
        A pandas DataFrame containing pykeen prediciton results plus two extra columns: either head/tail, head/relation or relation/tail, depending on what was provided as an input.
    id_table_head: pandas DataFrame
        A pandas DataFrame with two columns: 'id' and 'name'
    id_table_head: pandas DataFrame
        A pandas DataFrame with two columns: 'id' and 'name'

    Returns
    -------
    predictions: pandas DataFrame
        The same pandas DataFrame as the input DataFrame with items in the `heads` and `tails` columns renamed from IDs to common names.
    """

    # rename heads
    predictions = predictions.rename(columns = {'head': 'id'})
    predictions = predictions.merge(id_table_head)
    predictions = predictions.rename(columns = {'name': 'head'})
    predictions = predictions.drop(columns = ['id'])

    # rename tails
    predictions = predictions.rename(columns = {'tail': 'id'})
    predictions = predictions.merge(id_table_tail)
    predictions = predictions.rename(columns = {'name': 'tail'})
    predictions = predictions.drop(columns = ['id'])

    predictions = predictions.drop_duplicates()

    return(predictions)

def pipeline(model, training, heads = None, relations = None, tails = None):
    """Predict novel links in a Knowledge Graph from lists of heads/relations/tails. The main difference from pykeen.models.predict.get_prediction_df is that this function can work with lists.

    Parameters
    ----------
    model: object of pykeen.models class
        Embedding model used when running a pykeen pipeline.
    training: object of pykeen.triples.triples_factory.TriplesFactory class
        An object containing a training set corpredictionsponding to a dataset on which a model was trained.
    heads: list of strings
        List of graph heads.
    relations: list of strings
        List of graph relations.
    tails: list of strings
        List of graph tails.

    Returns
    -------
    predictions_all: pandas DataFrame
        A pandas DataFrame containing pykeen prediciton results plus two extra columns: either head/tail, head/relation or relation/tail, depending on what was provided as an input.
    """

    # Predict tails
    if heads and relations:
        if tails:
            print("Only two (not all three) of heads/relations/tails must be defined!")
            return(None)
        predictions_all = DataFrame()
        for h in heads:
            for r in relations:
                predictions = predict.get_prediction_df(
                    model = model, 
                    head_label = h, 
                    relation_label = r, 
                    triples_factory = training
                )
                predictions['head'] = h
                predictions['relation'] = r
                predictions_all = concat([predictions_all, predictions])
        
    
    # Predict relations
    if heads and tails:
        if relations:
            print("Only two (not all three) of heads/relations/tails must be defined!")
            return(None)
        predictions_all = DataFrame()
        for h in heads:
            for t in tails:
                predictions = predict.get_prediction_df(
                    model = model, 
                    head_label = h, 
                    tail_label = t, 
                    triples_factory = training
                )
                predictions['head'] = h
                predictions['tail'] = t
                predictions_all = concat([predictions_all, predictions])

    # Predict heads
    if relations and tails:
        if heads:
            print("Only two (not all three) of heads/relations/tails must be defined!")
            return(None)
        predictions_all = DataFrame()
        for r in relations:
            for t in tails:
                predictions = predict.get_prediction_df(
                    model = model, 
                    relation_label = r, 
                    tail_label = t, 
                    triples_factory = training
                )
                predictions['relation'] = r
                predictions['tail'] = t
                predictions_all = concat([predictions_all, predictions])

    return(predictions_all)

# run when file is directly executed
if __name__ == '__main__':

    # run examples with the Nations dataset
    result = pykeen_pipeline(
        model='TransE',
        dataset='Nations',
    )

    predictions = pipeline(result.model, result.training, heads = ['brazil'], tails = ['china'])
    print(predictions)
    predictions = pipeline(result.model, result.training, heads = ['brazil', 'uk'], tails = ['china', 'india'])
    print(predictions)
    predictions = pipeline(result.model, result.training, heads = ['brazil'], relations = ['relintergovorgs'])
    print(predictions.head())
    predictions = pipeline(result.model, result.training, relations = ['relintergovorgs'], tails = ['uk'])
    print(predictions.head())
    predictions = pipeline(result.model, result.training, heads = ['brazil'], relations = ['relintergovorgs'], tails = ['uk'])
    print(predictions)
