import pandas as pd


def load_abundance_gencode(fpath):
    df = pd.read_csv(fpath, sep='\t')
    target_attr = df.target_id.str.split('|', expand=True)
    target_attr.columns = ['gencode_tx', 'gencode_gene', 'havana_gene', 'havana_tx', 
        'hugo_tx', 'hugo_symbol', 'tx_length', 'gene_type', 'undefined']
    merged = df.join(target_attr)
    return merged[['gencode_tx', 'gencode_gene', 'hugo_symbol', 'gene_type', 
        'length', 'eff_length', 'est_counts', 'tpm']]


def merge_column(input_files, labels, data_col='est_counts'):
    """Merge Kallisto samples into a matrix

    Gather one column from all input_files into a single merged
    table, matching the index column to the first column of the 
    annotation file.
    """

    # Grab annotations from the first file
    fpath = input_files[0]
    df = load_abundance_gencode(fpath)
    annotations = df[['gencode_tx', 'gencode_gene', 'hugo_symbol', 'gene_type', 'length']]

    # Add the first file to the list
    sample_col = df[data_col]
    sample_col.name = labels[0]
    all_data = [df[data_col]]

    # Loop to add the rest
    for i, fpath in enumerate(input_files[1:]):
        sample_data = load_abundance_gencode(fpath)
        sample_col = sample_data[data_col]
        sample_col.name = labels[i]
        all_data.append(sample_col)

    # Merge columns into a single matrix
    merged = pd.concat(all_data, axis=1)

    # Use transcript ID as index
    merged.index = annotations['gencode_tx']
    
    # Sort columns
    merged = merged[sorted(merged.columns)]

    return annotations, merged