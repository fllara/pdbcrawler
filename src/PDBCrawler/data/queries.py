query_mw = '''{
  entries(entry_ids: [@IDS]) {
        rcsb_id,
    rcsb_entry_info {
      molecular_weight,
    }
  }
}'''

query_pol_entity = '''{
  entries(entry_ids: [@IDS]) {
        rcsb_id,
    rcsb_entry_info {
      molecular_weight,
    },
    pdbx_vrpt_summary {
      PDB_resolution
    },
    polymer_entities {
      entity_poly {
        pdbx_strand_id,
        pdbx_seq_one_letter_code_can
      },
      rcsb_polymer_entity_align {
        reference_database_name,
        reference_database_accession
      }
    }
  }
}'''