## Simulacra - Fake Data Synthesis

## Goals
This projects aims to help data scientists in easily creating fake datasets for algorithm testing, model validation and general purpose data generation (i.e. accelerators and education).

After conducting research, we found a similar framework had been developed in R called [simstudy](https://github.com/kgoldfeld/simstudy). We decided to translate the package and adapt it to our needs rather than starting from scratch.

A major usecase will be to generate _synthetic biased datasets_ in order to test how various algorithms perform with bias extraction and mitigation.

## Introduction to simstudy

Before generating synthetic data with simstudy, you first need to understand the two layers involved in the process:

1. __Data definition__, in which the user specifies the distribution she wishes to draw from, as well as its parameters. A neat feature of simstudy is the ability          for users to specify relationships between inputs and outputs very easily, by defining a variable as a function of another variable explicitely, or by              passing a correlation matrix as an argument.
2. __Data generation__, in which the user calls a set of functions to generate the data based on the definitions provided in the previous step

For an in-detail discussion about simstudy, please refer to the R package's original [documentation](https://kgoldfeld.github.io/simstudy/) as well as Keith Goldfeld's excellent [posts] (https://www.r-bloggers.com/author/keith-goldfeld/)

## How to use the package - generating biased synthetic data

A simple demo in which we define bias as an decreased (increased) likelihood of witnessing a succesful (unsuccesful) outcome due to being part of a certain group, holding all else equal.


### Scenario 1 - An Unbiased Loan Approval Data Generation Process

In __scenario 1__ we simulate a simple loan approval process using simstudy. In the first step, the _data definition_ step, we define a normally distributed *income_standardized* variable with a mean of 1 and a standard deviation of 1. This variable represents an individual's income as a Z-score - instead of taking its raw value, we express income in terms of its relative standard deviation.

We then simulate a loan approval process in which all individuals have a baseline 50% approval chance +/- income_standardized / 10. In essence, we are saying that every standard deviation increase is associated with a 10% probabilitiy increase of receiving a loan. Individuals on the higher (lower) end of the income scale are very (un)likely to receive a loan.

```python
df = defData(varname = "income_standardized", formula=0,
             variance=1, dist="normal")
 
# add a new data definition to previously defined data definition table
df = defData(df, varname="approval", formula='0.5*(income_standardized/10)', dist='binary')

# generate 10000 datapoints based on definitions
data = genData(10000, df)

```

### Scenario 2 - A Biased Loan Approval Data Generation Process

Now we simulate a biased approval process. We first generate a categorical column _category_ with 3 values, all with the same 33% probability of being drawn. 
We then use the _defCondition_ function to create biased approval process. When an individual's category is *blue*, her baseline approval is 40%, while others have a 50% baseline approval. This is a form of direct bias and can be picked up quite rapidly looking at summary statistics of tthe joint-distribution of color and approval.

```python
df2 = defData(varname = "category", formula="0.333, 0.333, 0.333",
             variance="red, blue, green", dist="categorical")

# add categorical data
data = addColumns(df2, data)

defC = defCondition(condition = "category=='blue'", formula = "0.4+income_standardized/10",
                    dist = "binary")

defC = defCondition(defC, condition = "category!='blue'", formula = "0.5+income_standardized/10",
                    dist = "binary")

# add a target column
data_biased = addCondition(defC, data, newvar="approval_bias")

data_biased.groupby('category')['approval_bias'].mean()
````

## Installation

**Use a personal auth token to download**

    git clone https://github.ibm.com/dse-rnd-incubator/simulacra-fake-data

**Create a working branch**

    git checkout -b "Branch-name"

**Before working, pull from master to update changes**

    git pull origin master

**After working in your local branch, add commit and push changes to your branch**

    'git add (insert filenames here)'
    'git commit -m "add comment message for commit"'
    'git push origin branch-name'
    
    We have not yet published this package, so the only way to use it is to install the repository onto your local machine via a github download. This is an internal project for now , so any contribution is welcome.

## Additional Information
Link to Box Folder:
https://ibm.ent.box.com/folder/154017733662

Use this style guide for python best coding practices.
https://www.python.org/dev/peps/pep-0008/

## Roadmap

1. Porting simstudy codebase to Python
2. Creating UI
3. Integrating more functionalities not included in simstudy from other packages or our own code