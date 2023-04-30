## Summary
- Engelhart generated a dataset of antibody mutants vs binding affinity to a covid peptide.
- Negative samples: "limit-of-blank", background subtraction (see Usage Notes / Binding to negative controls). Unless you have a strong reason to use these samples, they can be ignored.
- "scFv-format antibody": simplified antibody with only variable regions linked by a flexible chain instead of the rigid y-shaped "tail"


### To learn:
- BLI, esp "NGS-BLI curve"
- dissociation constant (kD) in absolute units (nM) [moles?] See fig 3a of Engelhart.
- https://github.com/facebookresearch/esm

- ESM notes
  - Which layer to user for embeddings?
    - so far using top layer (default) but tutorials use 33 and 34 as well
    - What about [zero-shot prediction?](https://www.biorxiv.org/content/10.1101/2021.07.09.450648v2) 
- in https://www.biorxiv.org/content/10.1101/2022.10.07.502662v1.full.pdf "Since the experimental assay on the initial antibody library was conducted in triplicate (each antibody sequence has 3 binding measurements), we either drop the assay with missing value or impute it with the median value of all assays of the same candidate chain. Then we take the average of all binding measurements corresponding to the same antibody." Not sure why they'd impute the median, as this NA implies a lower affinity, no the median affinity???


### Notes:
Q: Is this a “good” dataset of the local affinity fitness landscapes for these antibodies?
- Depends on:
  - complete exploration of sequence space, AA space. Need to consider variable length.
	- They explored every single-residue mutant of the CDRs, which is great, but also very conservative. The experiment seems very much a setup for another experiment. From my experience engineering GFP, epistasis was high, and Sarkisyan (2016) found mutants with k>10 that improved over WT.
	- Per [Wittmann et al. 2020](https://www.biorxiv.org/content/10.1101/2020.12.04.408955v1.full.pdf), it probably would have been more efficient to do some kind of zero-shot predictions and pre-screening. 
	- TODO: how good was the random k=2,3 mutation exploration?
	- TODO: Based on multi-residue mutants, is epistasis common?
  - Do plenty of mutants show improved fitness over WT? Don't want the vast majority to be non-functional; ideally, we capture some reasonably dense variance around the WT median affinity. And if nothing improves over WT, will be hard/impossible for models to extrapolate.
  - Are sequences indeed free or mostly free of indels?
  - General ML modeling questions: 
    - is there good sample/features ratio (not overwhelming curse of dimensionality)? If not, is it amenable to feature selection?
	- Want the one with high variance, reasonably high median binding, and low loss of function % among mutants.
		- Make good-performing model, and optimize its output
		- Use same model and select diverse sequences that predict to be WT
		- Don't necessarily need model here, select sequences with untried Amino-acid/position combination
		- OR if model includes some idea of variance, select sequences with highest variance in prediction.