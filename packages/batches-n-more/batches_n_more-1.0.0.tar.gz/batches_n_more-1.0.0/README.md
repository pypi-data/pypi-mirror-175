# batches_n_more

Unfortunately, PyPI cannot render some $\LaTeX$ instructions in this Markdown file properly. We suggest downloading the package, opening this `README.md` in VS Code and switching to the preview via <kbd>⇧ ⌘ V</kbd> (Mac) or <kbd>CTRL ⇧ V</kbd> (Unix, Windows) for a proper display.

## What can `batches_n_more` do?

Due to technical limitations of the GC/LC-MS platform, studies conducted on a large number of samples often need to be processed in multiple batches. The main variation in the resulting data does not come from biological variation, but can simply be explained by the batch affiliation of every single sample.

To deal with those batch effects, we propose the following pipeline:

1. Find features (i.e. distinct molecules defined by retention time $t$ and mass-to-charge ratio $m$) and align them into a so-called feature table, also called peak table; e.g., every row may correspond with a feature and every column with a sample. **Do this for every batch separately** with established state-of-the-art software like [`xcms`](http://www.bioconductor.org/packages/release/bioc/html/xcms.html) or [`MZMine 2`](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-395).

Since step 1 requires a lot of knowledge on chemistry and technical characteristics of the GC/LC-MS platform, we suggest this be done by people that are really familiar with these topics: the chemists and bioanalytics in labs, not data scientists.

The following two steps is where this package steps in:

2. Align multiple feature tables from different batches originating from the same experiment into one peak table. Difficulties we will almost certainly face here are shifts in retention time and mass-to-charge ratio for the same feature between different batches. 

3. Moreover, the mass spectrometer's sensitivity may vary from batch to batch; this is the main source for batch effects in the aligned peak table (apart from a poor alignment in step 2). Fight these batch effects, i.e. technically caused variability, while retaining biological variability between samples.

This means, after applying this package, you end up with a peak table comprising samples from all batches with little or no batch effect.

## Theoretical background on our methods

### Retention-time and mass-to-charge ratio shifts

Our correction method is based on so-called *anchors*. Anchors are sets of features we can uniquely identify with each other. 

In more detail: We begin by fixing a maximum retention-time and mass-to-charge ratio difference we are ready to tolerate for the same feature in different batches. These two numbers, called $\delta_{t}$ and $\delta_{m}$, heavily depend on your GC/LC-MS platform; you can inquire them from the colleagues in the lab. Note that you will always have to use the same units as in your initial feature tables for these two variables -- `batches_n_more` doesn't care about units. Let $N_b$ be the number of batches that our experiment comprises.

We build a network to find anchors: We draw a link between two features *from different batches* if they are *acceptable* for each other; *acceptable* again means that both retention times *and* mass-to-charge ratios lie within $\delta_{t}$ and $\delta_{m}$, respectively. We now want find all *isolated cliques* in this network that comprise as many features as we have batches, i.e., with exactly one feature per batch. In a network, 

* we call a subset of nodes *isolated* if every node in this subset is only linked to nodes that are also part of this subset -- quite a telling name. 
* Meanwhile, a *clique* is a subset of nodes from a network where every node of this subset is linked to any other node of this subset.

Consequently, an *anchor* is a subset with $N_b$ features where every feature possesses exactly one acceptible feature per batch. For an *anchor*, we can be quite sure that our alignment is correct because we lack other alternatives to align the features in an *anchor* differently.

We want identical features to have identical retention times and mass-to-charge ratios. For *anchors*, we can easily infer retention-time shifts: Consider an *anchor* comprising $N_b$ features with retention times $t_i, i = 1, ..., N_b$, and plot $t_i$ versus $t_1$ for every $i = 1, ..., N_b$. Doing this for every anchor we have found, produces $N_b$ plots. In a perfect world without retention-time shifts between batches, all plots would display an identity line whereas in the real world the points in every plots hover around the identity line. For the $i$-th plot, $i = 1, ..., N_b$, we interpolate the points with a two-times differentiable cubic spline $s_i$. Now, for *every* retention time $t$ from a feature in feature table $i$, $s_i(t)$ is the retention time we would have seen for this feature if it had been processed in batch $1$. Therefore, we correct $t$ by simply replacing it with $s_i(t)$.

For mass-to-charge ratios we apply the same procedure analogously.

After doing so, we still have $N_b$ separate feature tables, but we now have good reason to trust retention times and mass-to-charge ratios of all features: we have made them comparable.

### Aligning separate feature tables into one feature table

The approach we empower in this step is largely inspired by `BiPACE` as introduced in [Hoffmann, N., Keck, M., Neuweger, H. et al. Combining peak- and chromatogram-based retention time alignment algorithms for multiple chromatography-mass spectrometry datasets. BMC Bioinformatics 13, 214 (2012)](https://doi.org/10.1186/1471-2105-13-214).

First, we need a measure of similarity for every pair of two features $f_1 = (t_1, m_1), f_2 = (t_2, m_2)$, where $t_i, m_i, i = 1, 2$, are retention times and mass-to-charge ratios, respectively. We now want to find a similarity function $S: (0, \infty)^2 \to \mathbb{R} \cup \{ -\infty \}$ that indicates a higher degree of similarity between two features with a higher output. Moreover, it should yield $- \infty$ if

* $f_1$ and $f_2$ originate from the same batch (obviously, we don't want to align features from the same batch) or
* $| t_1 - t_2 | \geq \delta_{t}$ or $| m_1 - m_2 | \geq \delta_{m}$ (for technical reasons, we expect retention times and mass-to-charge ratios to deviate no more than our initially defined tolerances).

In all other cases, one might e.g. define $S$ to be

$$
S(f_1, f_2) = \frac{\delta_t - | t_1 - t_2 |}{\delta_t} \exp \left ( - \frac{(m_1 - m_2)^2}{2 \delta_m^2} \right ) \in (0, 1].
$$

Here, we weight deviations in retention time just linearly while we punish deviations in mass-to-charge ratio exponentially. This reflects the fact that mass-to-charge ratios are typically more stable between multiple batches.

Based on the similarity score we obtain from $S$, we can define batch-wise nearest neighbors for every feature in one of our original separate feature tables. More precisely, let $f$ be a feature from the $i$-th feature table, $i = 1, ..., N_b$. Then for $j = 1, ..., N_b, j \neq i$, we define $f$'s *nearest neigbor in batch $j$* to be the feature in batch $j$ with maximal similarity score among all features in batch $j$. Mathematically speaking, if $F_j$ is the set of all features from batch $j$, we have

$$
n_j(f) = \argmax_{g \in F_j} S(f, g).
$$

Again we want to build a network: Let $f_i, f_j$ be features from batch $i$ and $j$, respectively, with $i, j \in \{ 1, ..., N_b \}, i \neq j$. We connect two features $f_i, f_j$ in this network if and only if there is a *bidirectional best hit (BBH)* between $f_i$ and $f_j$. There is a *bidirectional best hit* between between $f_i$ and $f_j$ if $f_j$ is $f_i$'s nearest neighbor in batch $j$ *and vice-versa*. Demanding this best hit be bidirectional is crucial because a lot of naive approaches for alignment suffer from asymmetry, i.e., they treat one batch favorably.

Once we have built this network, we want to find all *maximal* cliques of size at least $k$, where we can choose $k \in \mathbb{N}, 2 \leq k \leq N_b$. A *maximal* clique is a clique which cannot be extended by another node withot losing the property of being a clique. In our case, such a maximal clique comprises $\ell$ features from $\ell$ different batches where every pair is a bidirectional best hit, $k \leq \ell \leq N_b$ and we cannot find another feature in one of the remaining batches that is a bidirectional best hit for *all* features already present in this maximal clique.

Basically, we now want to align the features in every maximal clique of size $k \leq \ell \leq N_b$ into one feature in our final feature table. For cliques of size strictly less than $N_b$, there will be samples in the final feature table (namely those from batches that are not represented by a feature in the clique) for which we don't have abundances; in these cases, we set them to be zero. Unfortunately, there is one little conflict remaining: One and the same feature can come up in more than one clique. Including them all into our final feature table would mean including one and the same feature several times -- a bad idea. For that reason, we start with aligning features from cliques without conflicts and we then mediate such conflicts.

To do so, we assess a clique $C = \{ f_i : i = 1, ..., \ell \}, k \leq \ell \leq N_b$, with features $f_i$ by assigning a goodness score

$$
G(C) = \sum_{\substack{f, g \in C\\ f \neq g}} S(f, g).
$$

We want larger cliques to be considered better; that's why we do not average over similarity scores in the above equation.

We then sort all cliques involved in a conflict by their goodness score in decreasing order. One strategy can now be:

* Start with the first clique in the ordered list and look up the features in it.
* Remove all cliques conflicting with the first clique, i.e. cliques that comprise one of the features in the first clique, from the list.
* Go to the next (remaining) clique in the list and repeat the procedure.

We end up with a set of non-conflicting cliques. We go through this set clique by clique and align the features from every clique into one feature; as a retention time and mass-to-charge ratio we take the mean over all retention times and mass-to-charge ratios of features in the clique, respectively.


### Correct batch effects

So far, we haven't changed at all the values, i.e. the abundances, in the feature tables; instead, we have only rearranged them. This changes in the last step where we want to get rid of batch effects in the aligned feature table. Let $A \in \mathbb{R}^{N_f \times N_s}$ be our aligned feature table with $N_f$ the number of features in it. To this end, `batches_n_more` provides two options.

#### Batch-wise fold changes via quality-control samples

For this method, we empower so-called quality-control samples (QCs) that are typically included in every batch of an experiment. Each QC is exactly the same substance measured as several samples in every batch. As a result, if there weren't batch effects, each feature would have exactly the same abundance in every QC. On the other hand, we can use the differences between QCs to infer systematic, technically caused differences between batches as follows.

1. For every batch $i, i = 1, ..., N_b$, calculate abundance medians feature-wise. That means we obtain median vectors $m_1, ..., m_{N_b} \in \mathbb{R}^{N_f}$.
2. Analyze median fold changes with batch $1$ as a reference: for $j = 1, ..., N_b$, calculate $f_j = m_1 / m_j \in \mathbb{R}^{N_f}$ element-wise.
3. Correct the aligned feature table to have all abundances expressed at the level of batch $1$: replace every sample in the aligned feature table, i.e. column vector, say $c \in \mathbb{R}^{N_f}$, belonging to the $j$-th batch with $c \cdot f_j$ element-wise. Do this for every $j = 1, ..., N_b$.

#### Principal-component analysis (PCA) and linear models

This second approach helps you two-fold: As the above heading promises, it corrects for batch effects. Additionally, it determines whether there any batch effects in the aligned feature table. Consequently, you can first apply the above approach to correct batch effects and then apply this approach to determine whether it was successful. This approach is largely taken from [Nyamundanda, G., Poudel, P., Patil, Y. et al. A Novel Statistical Method to Diagnose, Quantify and Correct Batch Effects in Genomic Studies. Sci Rep 7, 10849 (2017)](https://doi.org/10.1038/s41598-017-11110-6) and comprises these steps:

1. Choose some $N_{PC} \in \mathbb{N}, 1 \leq N_{PC} \ll N_f$, and project the columns of $A$ down to their first $N_{PC}$ principal components (PCs). This results in $A_0 \in \mathbb{R}^{N_{PC} \times N_s}$.
2. Try to predict PCs from just batch affiliation: Let $B \in \mathbb{R}^{N_s \times N_b}$ represent batch affiliation, i.e., 
   $$
   B_{i, \ell} = \begin{cases} 1 & \text{if sample $i$ is in batch $\ell$ or $\ell = N_b$},\\ 0 & \text{else}. \end{cases}
   $$
   That means we don't explicitly encode belonging to batch $N_b$ since it implicitly follows from not being part of batch $1, ..., N_b - 1$ and instead use the last column of $B$ for an intercept term in the linear model. We now fit $N_{PC}$ linear models via ordinary least-squares regression and end up with regression coefficients $C \in \mathbb{R}^{N_b \times N_{PC}}$ and residuals $\epsilon \in \mathbb{R}^{N_s, N_{PC}}$ to predict
   $$
   A_0^T = B C + \epsilon
   $$
   Keep in mind that the regression coefficients $C_{i, \ell}, i = 1, ..., N_b -1, \ell = 1, ..., N_{PC}$ express the difference in PC $\ell$ when belonging to batch $i$ instead of batch $N_b$. That means batch $N_b$ is the baseline level in our linear model.
3. *For coefficients that predict PCs well*, calculate the batch effect in the pricipal subspace, transform it back to original space and subtract it from $A$: To determine whether the linear models do a good job, we have a look at the p-test statistics for the regression coeffcients in $c$. We calculate them under the null hypothesis that there is no link between batch affiliation and the PC. We select a threshold $t_p \in (0, 1)$ and modify $C$ into $C_0$ as follows:
   $$
   (C_0)_{i, \ell} = \begin{cases} 0 & \text{if corresponding p-test statistic is above $t_p$ or $i = N_b$},\\ C_{i, l} & \text{else}. \end{cases}
   $$
   Calculate the batch effects in the subspace of the first $n_{PC}$ PCs via
   $$
   A_1^T = B C_0
   $$
   and perform a PCA-reverse transform of $A_1$, which yields $A_2 \in \mathbb{R}^{N_f \times N_s}$, the batch effects in the orginal space. Finally,
   $$
   A - A_2
   $$
   is our feature table without batch effects.

`batches_n_more` will report the p-test statistics for the regression coefficients in $C$. There are no batch effects on the data according to the ordinary linear model if and only if all p-test statistics are insignificant.

## How to use `batches_n_more`

`batches_n_more` not only implements the above approach in an easy-to-use manner. It also provides routines for file input and output as well as for often-needed visualizations such as 2-dimensional PCA plots, plots of retention time shifts or heatmaps of pairwise correlations between samples.

### A detailed code example

We start by reading the feature tables of three batches of the same experiment. Each feature table is stored as an Excel `.xlsx` file; we are interested in the second sheet of every file called `inputR` where we have features in the rows and samples in the columns. The first row holds sample names, and the first column holds information on the features and is of the form `mz:73.52864_rt:0.97619`.

```python
import batches_n_more as bnm

dir = "data/example/"
files = ["First_batch.xlsx", "Second_batch.xlsx", "Third_batch.xlsx"]
Pt_list = []
for i, filename in enumerate(files):
    filepath = dir + filename
    Pt = bnm.read_pt_excel(
        filepath,
        sheet_name = ["inputR"], # if all feature tables are in the same file as several sheets,
        # you only need to specify them all in a list 
        rt_ident = "rt:",
        mz_ident = "mz:",
        qc_ident = None # here, all samples are QC samples
    )
    # plot histogram of retention times to get an idea of their distribution.
    # for our retention-time and mass-to-charge ratio correction approach it's
    # best to have them as uniformly as possible distributed
    Pt[0].rt_hist("results/mz_rt_histograms/rt_batch" + str(i) + ".pdf")
    Pt[0].mz_hist("results/mz_rt_histograms/mz_batch" + str(i) + ".pdf")
    Pt_list += Pt
```

Output:

```
data/example/First_batch.xlsx | shape: (1113, 9)
data/example/Second_batch.xlsx | shape: (1114, 5)
data/example/Third_batch.xlsx | shape: (1417, 13)
```

Reading the data is probably the nastiest part of using `batches_n_more` because there are many ways to store feature tables, but let's go through it: `batches_n_more.read_pt_excel()` expects samples as columns; retention-time as well as mass-to-charge ratio identifiers need to be in the first column and sample names (possibly with a QC identifier) in the first row. For details have a look at the documentation: `help(bnm.read_pt_excel)`. This is a format you easily get from `MZMine 2`. If you don't have data in the desired format, you may consider manipulating it first: directly in Excel or -- if there are more files or there is more to do -- with a little program written in Python or R, e.g.

`batches_n_more.read_pt_excel()` returns a list of `Peaktable`s, the basic class of `batches_n_more`, which stores, manipulates and visualizes feature tables. Next we will put them into an instance of the `Peaktable_align` class, which basically holds multiple feature tables and does all of the work related to alignment.

```python
Pt_align = Peaktable_align(
    Pt_list,
    mz_tol = 0.003, # \delta_m in the above section, for the GC-MS platform in this example: 0.003 [millidalton]
    rt_tol = 0.25 # \delta_t in the above section, here: 0.25 [minutes]
)
```

$\delta_m$ = `mz_tol` and $\delta_t$ = `rt_tol` are all we need to well-define the search for anchors, so we proceed with correcting shifts in retention time and mass-to-charge ratio.

```python
Pt_align.find_anchors()
for mz_or_rt in ["mz", "rt"]:
    Pt_align.plot_shift(mz_or_rt, filepath = "results/" + mz_or_rt + "_shift.pdf")
Pt_align.interpolate()
Pt_align.correct_mz_rt()
```

Output:

```
Found 459 mz anchors and 310 rt anchors
```

Continue with aligning the three feature tables and do some first analysis concerning batch effects.

```python
Pt_aligned = Pt_align.align(k_min = 2, mediator = "caesar")
# mediator "caesar" for conflicts between samples is intoduced in "Theoretical background on methods".
# mediator "solon" is more concerned with common good and less aggressive
Pt_aligned.plot_pca_2d(filepath = "results/pca_after_align.pdf") # plot unveils heavy batch effects
Pt_aligned.correlation_heatmap("results/corr_after_align.pdf")
# a troughout high correlation suggests batch effects are not that hard to tackle: 
# there is a simple linear link
```

Output:

```

Overview on clique sizes BEFORE removing duplicates
   size 2  size 3  total
#     342     712   1054
Overview on clique sizes AFTER removing duplicates
   size 2  size 3  total
#     328     712   1040
Aligned peak table has shape (1040, 27)
```

In this example, we only lose 14 cliques when we give `"caesar"` the *imperium* to mediate conflicts. We barely lose features compared to `First_batch.xlsx` with 1113 features. Finally, we deal with batch effects. We will first apply the method "Batch-wise fold changes via quality-control samples" or the `qc_fold_correct` method of `Peaktable` to tackle batch effect. Afterwards we will do some checks with the `batch_correct` method and plots.

```python
Pt_aligned.qc_fold_correct()
Pt_aligned.batch_correct()
Pt_aligned.plot_pca_2d(filepath = "results/pca_after_batch_correction.pdf")
Pt_aligned.correlation_heatmap(filepath = "results/corr_after_batch_correction.pdf")
```

Output:
```

p values for regression coeffcients in batch correction
(under null hypothesis that there is no link between batch and PC):
     batch 2 vs. 0  batch 2 vs. 1  batch 2 vs. 2
PC1            1.0            1.0            1.0
PC2            1.0            1.0            1.0
PC3            1.0            1.0            1.0
```

`Peaktable.batch_correct` reveals no more batch effects: all regression coefficients are totally plausible under the assumption that there is no link between batch affiliation and PCs, meaning we cannot predict PCs from batch affilliation via a linear model. As a result, `Peaktable.batch_correct` does not step in and does not manipulate the data at all. Unlike in the previous PCA plot, in the current one there no more batch-wise clusters visible. The correlation heatmap reveals even stronger correlation between all samples. For its part, `batches_n_more` is done, so we can store the aligned feature table.

```python
Pt_aligned.write_excel("results/aligned.xlsx")
```

### A code example that uses wrappers

The above example is important to understand the single steps `batches_n_more` takes in aligning feature tables and battling batch effects and it reveals the structure of `batches_n_more`. Yet, in a use case, you would always leave certain parts of the above example unchanged. This is where two wrappers of `batches_n_more` get interesting, they condense several lines of the above code into one line and one command.

* `Peaktable_align.align_wrapper()` takes the entire step 2 in the above section "What `batches_n_more` can do": find anchors, interpolate shifts in retention time and mass-to-charge ratio, correct them and actually align multiple batches into one feature table.
* `Peaktable.batch_correct_wrapper()` takes the entire step 3 in "What `batches_n_more` can do": first apply qc_fold_correct(), then batch_correct() looks for batch effects on the resulting feature table and, if it finds batch effects, corrects them.

```python
# loading data must remain rather lengthy: it is highly individual for each data set
dir = "data/example/"
files = ["First_batch.xlsx", "Second_batch.xlsx", "Third_batch.xlsx"]
Pt_list = []
for i, filename in enumerate(files):
    filepath = dir + filename
    Pt = read_pt_excel(
        filepath,
        sheet_name = ["inputR"],
        rt_ident = "rt:",
        mz_ident = "mz:",
        qc_ident = None
    )
    Pt_list += Pt

Pt_align = Peaktable_align(
    Pt_list,
    mz_tol = 0.003,
    rt_tol = 0.25
)

# from this line forward, wrappers step in
Pt_aligned = Pt_align.align_wrapper(
    k_min = 2,
    mediator = "caesar",
    plot_dir = "results"
    )
Pt_aligned.batch_correct_wrapper(
    n_pcs = 3,
    significance_threshold = 0.05,
    plot_dir = "results"
    )

Pt_aligned.write_excel("results/aligned.xlsx")
```