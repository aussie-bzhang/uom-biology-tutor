**Chapter 27**

Regulation of Gene Expression

*Application Problems - Review Questions*

For: Zhang Wentao | University of Melbourne

*This set of 5 application problems is designed to test your understanding of gene expression regulation mechanisms covered in Lecture 27. Each question involves experimental analysis, calculations, or data interpretation. Answer all questions in the spaces provided, then check your answers against the Answer Key at the end of this document.*

**Question 1: Lac Operon Combinatorial Control - Expression Calculation**

*[15 points]*

The lac operon in E. coli is regulated by both the LacI repressor (negative control) and the CAP-cAMP activator (positive control). The expression level of the lac operon depends on the presence or absence of glucose and lactose in the growth medium. The basal (uninduced) expression level is approximately 1 unit. When fully induced (lactose present, glucose absent), expression reaches 100 units. CAP-cAMP binding increases transcription efficiency 50-fold, while the presence of the LacI repressor reduces transcription to the basal level.

Consider an E. coli strain with a wild-type lac operon. Complete the table below by calculating the relative expression level (in arbitrary units) of beta-galactosidase under each growth condition. Show your reasoning for each condition.

| **Glucose** | **Lactose** | **Expression Level** | **Brief Explanation** |
| --- | --- | --- | --- |
| Present | Absent |  |  |
| Present | Present |  |  |
| Absent | Absent |  |  |
| Absent | Present |  |  |

(b) A mutant E. coli strain has a deletion in the CAP binding site. Predict the expression level of this mutant when grown in a medium containing only lactose (no glucose). Explain your answer.

(c) Another mutant has a non-functional LacI repressor (cannot bind operator). Predict the expression level when this mutant is grown in a medium containing both glucose and lactose. Explain your answer.

**Question 2: DNA Methylation and Phenotypic Plasticity - Experimental Design**

*[15 points]*

Queen bees and worker bees are female honeybees that develop from genetically identical larvae (both have two X chromosomes). However, queen bees are larger, fertile, and have longer lifespans. Research has shown that royal jelly, which is fed exclusively to queen larvae, contains inhibitors of DNA methyltransferases (DNMTs). This differential DNA methylation pattern leads to different gene expression profiles and distinct phenotypes.

(a) Design an experiment to test the hypothesis that differential DNA methylation at CpG islands in the promoter region of a specific gene (e.g., the insulin-like growth factor gene, AmILP1) is responsible for the size difference between queen and worker bees. Your experimental design should include:

* A clear statement of your experimental and control groups
* The specific molecular technique you would use to analyze DNA methylation (justify your choice)
* The predicted results if your hypothesis is correct
* One potential confounding factor and how you would control for it

(b) In the experiment described by Kucharski et al. (2008), treatment of newly hatched larvae with a DNMT inhibitor (such as those found in royal jelly) resulted in the development of queen-like traits in genetically worker-destined bees. If the AmILP1 promoter normally has 12 CpG sites that are 90% methylated in workers and only 20% methylated in queens, calculate the expected change in methylation percentage at these sites after DNMT inhibition. Show your work.

(c) Explain why DNA methylation at promoter CpG islands typically results in gene silencing. Describe the molecular mechanism involving histone modifications.

**Question 3: Transcription Factor Binding Kinetics and Gene Regulation**

*[15 points]*

The LacI repressor binds to the operator sequence (O1) of the lac operon with a dissociation constant Kd = 0.1 pM (picomolar). The repressor exists as a homotetramer in solution and binds to the operator as a tetramer. The intracellular concentration of LacI in E. coli is approximately 10 molecules per cell, and the volume of an E. coli cell is approximately 1 femtoliter (1 x 10^-15 L).

(a) Calculate the intracellular concentration of LacI in nanomolar (nM). Show your calculation steps. (Avogadro's number = 6.022 x 10^23 molecules/mol)

(b) Using the formula for fractional occupancy: theta = [LacI] / ([LacI] + Kd), calculate the fraction of lac operon operators that are bound by LacI repressor under the following conditions. Assume Kd remains constant.

| **Condition** | **[LacI]** | **Fractional Occupancy** |
| --- | --- | --- |
| Basal (no IPTG) | Your answer from (a) |  |
| After 1000-fold dilution |  |  |
| When IPTG binds LacI (Kd increases 1000x) | Same as (a) |  |

(c) IPTG (isopropyl-beta-D-thiogalactopyranoside) is a non-metabolizable analog of allolactose that binds to the LacI repressor. When IPTG binds LacI, the repressor's affinity for the operator decreases 1000-fold. Explain how this molecular interaction leads to increased expression of the lac operon, and calculate the new Kd in the presence of IPTG.

(d) If the presence of IPTG increases the Kd by 1000-fold (to 100 pM), what is the new fractional occupancy of the operator? Is the operon primarily ON or OFF under this condition? Explain.

**Question 4: Gene Expression Profiling: Microarray vs. RNA-seq Data Analysis**

*[15 points]*

You are studying the dimorphic fungal pathogen Penicillium marneffei, which switches between yeast and hyphal growth forms depending on temperature. You want to compare gene expression profiles between the two growth forms to identify temperature-regulated genes. You have isolated total RNA from both yeast-form (37 deg C) and hyphal-form (25 deg C) cultures.

(a) You perform an RNA-seq experiment and obtain the following normalized read counts for four key regulatory genes. Calculate the fold change (log2) for each gene and determine which genes are upregulated or downregulated in yeast form compared to hyphal form. A gene is considered differentially expressed if |log2(fold change)| > 1 and the normalized count is > 50 in at least one condition.

| **Gene** | **Yeast (37 C)** | **Hyphal (25 C)** | **Log2(FC)** | **DE?** |
| --- | --- | --- | --- | --- |
| hgrA | 1,250 | 45 |  |  |
| brlA | 30 | 890 |  |  |
| abaA | 15 | 340 |  |  |
| wetA | 5 | 120 |  |  |

(b) You also perform a microarray experiment using the same RNA samples. In the microarray data, you find that the fluorescence intensity ratio (Cy5/Cy3) for hgrA is 28.5, but for a housekeeping gene (actin) the ratio is 1.1. Explain why actin is used as a control in microarray experiments, and calculate the normalized expression ratio of hgrA relative to actin.

(c) Compare the sensitivity and dynamic range of RNA-seq versus microarray technology. Which technique would be more suitable for detecting low-abundance transcripts, and why? Provide a quantitative justification (consider that microarrays have a dynamic range of approximately 2-3 orders of magnitude, while RNA-seq has 4-5 orders of magnitude).

**Question 5: Multi-level Gene Regulation in Eukaryotes - Integrated Analysis**

*[15 points]*

In eukaryotic cells, gene expression can be regulated at multiple levels: chromatin remodeling, transcriptional control, RNA processing, nuclear export, mRNA stability, translational control, and post-translational modification. Each level provides an opportunity to amplify or attenuate the final amount of functional gene product.

Consider a eukaryotic gene that produces a critical metabolic enzyme. Under baseline conditions, the gene produces 1,000 mRNA transcripts per hour, and each mRNA has a half-life of 2 hours. The translation efficiency is 10 protein molecules per mRNA per hour, and the protein has a half-life of 4 hours.

(a) Calculate the steady-state number of mRNA molecules in the cell. Assume first-order decay kinetics where the decay rate constant k = ln(2) / t\_half. (Hint: At steady state, synthesis rate = degradation rate)

(b) Calculate the steady-state number of protein molecules in the cell, assuming that all mRNA molecules are equally translationally active.

(c) The cell encounters a stress condition that triggers a cascade of regulatory events:

* Chromatin remodeling opens the promoter region, increasing transcription 5-fold
* A microRNA is induced that reduces mRNA half-life to 30 minutes
* A translational repressor protein reduces translation efficiency to 2 protein molecules per mRNA per hour
* The protein becomes stabilized, with a new half-life of 8 hours

Calculate the new steady-state mRNA and protein levels under stress conditions. Show all steps.

(d) By what overall factor did the protein level change from baseline to stress conditions? Which regulatory step (transcription, mRNA stability, translation, or protein stability) contributed most significantly to the final change in protein levels? Provide a quantitative analysis comparing the contribution of each regulatory level.

**ANSWER KEY**

*The following answers are provided for self-checking purposes. Partial credit may be awarded for correct reasoning even if final calculations contain minor errors.*

**Question 1: Lac Operon Combinatorial Control**

**Part (a) - Expression Table**

| **Glucose** | **Lactose** | **Expression** | **Explanation** |
| --- | --- | --- | --- |
| Present | Absent | ~1 unit | LacI bound (no allolactose); CAP not active (high glucose = low cAMP) |
| Present | Present | ~1 unit | LacI still bound (allolactose not efficiently transported); CAP inactive |
| Absent | Absent | ~1 unit | LacI bound; CAP active but repressor blocks transcription |
| Absent | Present | ~100 units | LacI released; CAP-cAMP strongly activates transcription |

**Part (b) - CAP Binding Site Deletion**

The expression level would be approximately 2 units (basal level x 2). Without the CAP binding site, positive activation by CAP-cAMP cannot occur. Even though LacI is removed by allolactose binding, RNA polymerase can only transcribe at a low basal level (~2-fold above fully repressed). This demonstrates that full induction requires both: (1) removal of the repressor, AND (2) activation by CAP-cAMP.

**Part (c) - Non-functional LacI Mutant**

The expression level would be approximately 2-5 units (intermediate). Without functional LacI, the operator is always unoccupied, allowing basal transcription. However, because glucose is present, cAMP levels are low and CAP cannot activate transcription efficiently. The operon shows constitutive low-level expression (leaky expression). This is higher than wild-type with glucose + lactose (~1 unit) because there is no repressor blocking the promoter at all.

**Question 2: DNA Methylation and Phenotypic Plasticity**

**Part (a) - Experimental Design**

Experimental groups: Collect newly hatched larvae and divide into: (1) Control group - fed standard worker jelly (expected to develop into workers), and (2) Treatment group - fed royal jelly or jelly supplemented with DNMT inhibitor (expected to develop queen-like traits).

Technique: Bisulfite sequencing (BS-seq) is the gold standard. Sodium bisulfite converts unmethylated cytosines to uracil, while methylated cytosines remain unchanged. After PCR amplification and sequencing, the methylation status at each CpG site can be determined by comparing to the reference genome.

Predicted results: The AmILP1 promoter in the treatment group (royal jelly/DNMT inhibitor) will show significantly lower CpG methylation compared to the control group. Lower methylation correlates with higher AmILP1 expression and larger body size.

Confounding factor: Nutritional differences between royal jelly and worker jelly (not just DNMT inhibitors) could affect growth. Control: Use worker jelly supplemented with a specific DNMT inhibitor (e.g., 5-aza-2'-deoxycytidine) as an additional treatment group to isolate the methylation effect.

**Part (b) - Methylation Calculation**

Worker methylation: 90% of 12 CpG sites = 10.8 sites methylated on average. Queen methylation: 20% of 12 CpG sites = 2.4 sites methylated. Expected change after DNMT inhibition in workers: DNMT inhibition should block new methylation and cause passive demethylation during cell division. Expected final methylation: approaching 20% (queen-like level) or lower. Change = 90% - 20% = 70 percentage point decrease in methylation. This represents a 3.5-fold relative decrease in methylation (90/20 = 4.5, or 77.8% reduction).

**Part (c) - Mechanism of Silencing**

DNA methylation at promoter CpG islands recruits methyl-CpG binding domain proteins (MBDs), such as MeCP2. These MBDs interact with histone deacetylases (HDACs) and histone methyltransferases that deposit repressive marks (H3K9me3 and H3K27me3). The deacetylation of histone tails increases the positive charge of histones, strengthening their interaction with negatively charged DNA, resulting in a more compact chromatin structure (heterochromatin). This physically blocks the binding of transcription factors and RNA polymerase to the promoter, leading to transcriptional silencing.

**Question 3: Transcription Factor Binding Kinetics**

**Part (a) - Intracellular [LacI]**

Concentration = (number of molecules) / (Avogadro's number x volume in L)

[LacI] = 10 / (6.022 x 10^23 x 1 x 10^-15)

[LacI] = 10 / (6.022 x 10^8) = 1.66 x 10^-8 mol/L = 16.6 nM

**Part (b) - Fractional Occupancy**

Condition 1 (Basal): theta = 16.6 nM / (16.6 nM + 0.0001 nM) = 16.6 / 16.6001 = 0.999994 (approximately 1.0 or 100%)

Condition 2 (1000-fold dilution, [LacI] = 0.0166 nM): theta = 0.0166 / (0.0166 + 0.0001) = 0.0166 / 0.0167 = 0.994 (99.4%)

Condition 3 (IPTG present, Kd = 100 pM = 0.1 nM): theta = 16.6 / (16.6 + 0.1) = 16.6 / 16.7 = 0.994 (99.4%)

**Part (c) - IPTG Mechanism**

IPTG is an allolactose analog that binds to the allosteric site of the LacI repressor. This binding causes a conformational change in the repressor protein, reducing its affinity for the operator DNA sequence by 1000-fold. The new Kd = 0.1 pM x 1000 = 100 pM = 0.1 nM. When the repressor's affinity drops, it dissociates from the operator, allowing RNA polymerase to access the promoter and initiate transcription.

**Part (d) - Operon Status with IPTG**

New Kd = 100 pM = 0.1 nM. With [LacI] = 16.6 nM:

theta = 16.6 / (16.6 + 0.1) = 16.6 / 16.7 = 0.994

Wait - this suggests high occupancy. However, IPTG also reduces the effective concentration of active repressor because IPTG-bound LacI cannot bind DNA. The effective [LacI\_free] = [LacI\_total] / (1 + [IPTG]/Kd\_IPTG). With saturating IPTG, essentially all LacI is in the IPTG-bound form and cannot bind DNA. Therefore, theta approaches 0, and the operon is fully ON. The correct interpretation is that IPTG sequesters the repressor, making it unavailable for DNA binding.

**Question 4: Gene Expression Profiling**

**Part (a) - RNA-seq Analysis**

| **Gene** | **Yeast** | **Hyphal** | **Log2(FC)** | **DE?** |
| --- | --- | --- | --- | --- |
| hgrA | 1,250 | 45 | +4.80 | Yes (up) |
| brlA | 30 | 890 | -4.89 | No |
| abaA | 15 | 340 | -4.50 | No |
| wetA | 5 | 120 | -4.58 | No |

Calculation example for hgrA: Log2(1250/45) = Log2(27.78) = 4.80. hgrA is the only gene meeting the DE criteria (|log2FC| > 1 AND count > 50 in at least one condition).

**Part (b) - Microarray Control**

Actin is used as a normalization control because it is a housekeeping gene expressed at relatively constant levels across different conditions and cell types. It corrects for technical variations in RNA labeling, hybridization efficiency, and scanning. Normalized ratio = (hgrA ratio) / (actin ratio) = 28.5 / 1.1 = 25.9-fold upregulation in yeast form.

**Part (c) - Technique Comparison**

RNA-seq is more suitable for detecting low-abundance transcripts. Microarrays have a dynamic range of 10^2 to 10^3 (2-3 orders of magnitude), limited by background fluorescence saturation and probe cross-hybridization. RNA-seq has a dynamic range of 10^4 to 10^5 (4-5 orders of magnitude), limited only by sequencing depth. For a transcript present at 1 copy per cell, RNA-seq can detect it with sufficient read depth, while microarrays may not distinguish it from background noise. Additionally, RNA-seq can detect novel transcripts and splice variants, while microarrays are limited to pre-designed probes.

**Question 5: Multi-level Gene Regulation**

**Part (a) - Steady-State mRNA**

k\_mRNA = ln(2) / 2 hr = 0.347 hr^-1. At steady state: d[mRNA]/dt = 0 = k\_synthesis - k\_degradation x [mRNA]. Therefore: [mRNA]\_ss = k\_synthesis / k\_degradation = 1000 transcripts/hr / 0.347 hr^-1 = 2,882 mRNA molecules.

**Part (b) - Steady-State Protein**

First, calculate protein synthesis rate: 2,882 mRNA x 10 proteins/mRNA/hr = 28,820 proteins/hr. k\_protein = ln(2) / 4 hr = 0.173 hr^-1. [Protein]\_ss = 28,820 / 0.173 = 166,589 protein molecules.

**Part (c) - Stress Conditions**

New transcription rate = 1000 x 5 = 5,000 transcripts/hr.

New k\_mRNA = ln(2) / 0.5 hr = 1.386 hr^-1.

New [mRNA]\_ss = 5,000 / 1.386 = 3,608 mRNA molecules.

New protein synthesis rate = 3,608 x 2 = 7,216 proteins/hr.

New k\_protein = ln(2) / 8 = 0.087 hr^-1.

New [Protein]\_ss = 7,216 / 0.087 = 82,943 protein molecules.

**Part (d) - Regulatory Contribution Analysis**

Overall change: 82,943 / 166,589 = 0.50-fold (50% of original, or a 2-fold decrease).

Individual contributions if other factors held constant:

* Transcription increase alone (5x): would increase protein 5-fold
* mRNA stability decrease alone (2 hr to 0.5 hr): would decrease mRNA 4-fold, decreasing protein 4-fold
* Translation decrease alone (10 to 2): would decrease protein 5-fold
* Protein stability increase alone (4 to 8 hr): would increase protein 2-fold

The decrease in translation efficiency (5-fold decrease) and the decrease in mRNA stability (4-fold decrease) are the dominant factors. Together: 5 x (1/4) x (1/5) x 2 = 0.5-fold. The transcription increase and protein stability increase partially compensate but cannot overcome the strong negative effects at the mRNA stability and translation levels. The most significant contributor to the net decrease is the combination of reduced mRNA stability and reduced translation efficiency.