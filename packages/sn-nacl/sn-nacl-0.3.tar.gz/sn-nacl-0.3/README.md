# NaCl 

The `NaCl` package contains code to develop and train type Ia
supernova spectrophotometric models.  The training is implemented as a
likelihood minimization (under constraints).

`NaCl` stands for /Nouveaux algorithmes de Courbes de lumiere/ (french
for /New lightcurve algorithms/).

As of today, the `NaCl` package contains a (1) re-implementation of
the SALT2 model and error model (Guy et al, 2007), with various
improvements to make sure that the training can be performed in one
single minimization (2) classes to manage a hybrid (light curves +
spectra) training sample (3) a minimizer to perform the minimization
of the SALT2 log-likelihood.


## Installation

### With pip

`NaCl` can be installed with pip:

```bash
pip install sn-nacl 
```

Depending on your version of python, you may run into trouble with the
installation of `scikit-sparse`.  The package generally needs numpy to
be installed already (and doesn't fetch it automatically if missing).
Also, for python>=3.10, the pip installation of scikit-sparse may
complain about various things and stops.  If you encounter this kind
of problem, this longer install sequence should work:

```bash 
pip install numpy
git clone https://github.com/scikit-sparse/scikit-sparse.git
cd scikit-sparse; python setup.py install; cd ..
pip install sn-nacl
```


### Compile from source 

You may prefer to clone the repository and compile it directly from source. 

```bash
git clone https://gitlab.in2p3.fr/cosmo/nacl.dev.git  # change repo name !
python setup.py install [--user]
```
or, 
```bash
pip install . 
```

or, if you intend to hack the code, and prefer to work with an editable install:
```bash
pip install -e . 
```

### Building the documentation 

First make sure you have sphinx installed: 
```bash
pip install sphinx_gallery sphinx_rtd_theme
```
then 
```bash
$ cd docs
$ make html  # for example 
```
type 
```bash
$ make 
```
for a list of targets. 


## Testing

```bash 
$ cd salt3.dev
$ pytest-3
```


In ipython3 :
run script_modules.py --> will ask : -data you want to analyse, for simulation give 'simulation' for real CSP data give 'csp'
     		      	       	     -Number of SNe to consider.

		      --> will plot : - data, flux model & error model fit in upper panel and data, flux model fit in bottom pannel.
		      	       	      - chi2, of the 2 fits (interractive plot, click on blue cross)
				      - corrected light curves.
				      - error model parameter histogram. 

in salt3.dev/sandbox:

run spectrum_recalibration.py

m = fit_simulation(surveys= ['csp', 'snls']) : will run the salt2-like model on a JLA_like simulation


m = fit_simulation(surveys = ['csp'], zcut = 1., mu_reg=100, variance=1, model_coef_init= 0.9, var_coef_init=1.5)
