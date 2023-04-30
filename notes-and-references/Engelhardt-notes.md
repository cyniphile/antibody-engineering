# abstract
  - start with three seed sequences (identified using phage display)

# BG and Summary

- it's good to generate *labeled* data.
- want to sample and quantify the target space robustly, not just focus on winners/"binders"
- Used phage display to find three wt antibodies that stick to a target covid peptide
- In silico designed all single-residue mutants plus random k=2,3 mutants

# Methods

 - Target sequence "PDVDLGDISGINAS" is highly conserved part of covid spike.
 - Heavy chain vs light chain "orientation"? HL vs LH is interchangeable in scFv
   - "chain orientation had little to no effect on binding affinity with all but Ab-91-HL (3.39 nM) resulting in predicted KD values below 1 nM. The best chain orientation was selected for each antibody; HL was selected for Ab-14, LH was selected for Ab-91 and HL was selected for Ab-95"
- All k=1 mutations made + some random k=2,3 in CDRs.
  - "indels were avoided to ensure the amino acid sequence was constant length." True within libraries
  -  "up to k = 3 mutations were chosen to guarantee there was at least one instance where one amino acid substitution occurred in all CDRs of a given chain at a given time." They wanted at least one example (for each of the two chains, H and L) where there was a sub in all the three CDRs of that chain.
  -  "The number of variants for k = 1 mutations was determined based on the combined number of amino acid positions in the CDRs of a given chain and the total number of possible amino acid substitutions in each position." Subs possible at each position is always 19 no? Math not quite working out for me, I get 660 for 14 heavy, and that's using 20 subs (I think 19 makes more sense because identity sub doesn't count)
  -  "All k = 1 variants were kept, ensuring that duplicates and original chain sequences were removed. Using the number of sequence variants for k = 1, a scaling factor of ~6 was applied to determine the number of variants to sample from the total number of k = 2 and k = 3 possible sequence variants, as shown in Table" So they take the number of possible variants for k=1 mutation, and keep k * ~6 as many for higher mutation counts. Again, math not quite working out for me 6.06 * 665 = 4029 (not 4089)?
- Some designs were not successfully assayed (104k / 119k)
- "target binding was subsequently measured with 71,384 designs resulting in a predicted affinity value for at least one of the triplicate measurements. Seems like they only got measurements for 71k designs? And they measured 3 times.

## Alpha-seq data collection
- put plasmids with antibodies into yeast