import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

def mod_diagnostics(model, data):
    """
    Output to file model diagnostics for an OLS model

    Input:
        model - statsmodels.regression.linear_model.OLS object
        data  - pandas.DataFrame containing data for model

    Output:
        XX-XX-OLS_SampleXX_Summary.txt contains the model summary output
        XX-XX-OLS_SampleXX_ResidHist.png is histogram of the residuals
        XX-XX-OLS_SampleXX_StdResid.png is a plot of standardised residuals against fitted values

        if model is univariate: XX-XX_OLS_SampleXX_Regression.png is a scatter plot with regression line

    Requires:
        statsmodels.api
        pandas
        numpy
        plt.pyplot
    """

    fitted = model.fit()
    dep = model.endog_names
    indep_names = ""

    # create a string containing list of indep names for output files
    for name in model.exog_names[1:]:  # we don't want 0 element as that is the intercept
        indep_names += "{0}_".format(name)

    # Want to include name of DataFrame in the output filename but currently DataFrame does not have a name attribute
    # So for now use nobs from fitted
    samplesize = str(int(fitted.nobs))

    f1 = open("{0}-{1}OLS_Sample{2}_Summary.txt".format(dep, indep_names, samplesize), "w")
    f1.write(fitted.summary().as_text())
    f1.close()

    # calculate standardized residuals ourselves
    fitted_sr = (fitted.resid / np.std(fitted.resid))

    # Histogram of residuals
    ax = plt.hist(fitted.resid)
    plt.xlabel('Residuals')
    plt.savefig('{0}-{1}OLS-Sample{2}_ResidHist.png'.format(dep, indep_names, samplesize), bbox_inches='tight')
    plt.close()

    # standardized residuals vs fitted values
    ax = plt.plot(fitted.fittedvalues, fitted_sr, 'bo')
    plt.axhline(linestyle='dashed', c='black')
    plt.xlabel('Fitted Values')
    plt.ylabel('Standardized Residuals')
    plt.savefig('{0}-{1}OLS-Sample{2}_StdResid.png'.format(dep, indep_names, samplesize), bbox_inches='tight')
    plt.close()

    # add code here for a q-q plot??


    if (len(model.exog_names) == 2):  # univariate model (with intercept)

        indep = model.exog_names[1]

        # scatter plot with regression line
        ax = plt.plot(data[indep], data[dep], 'bo')
        x = np.arange(data[indep].min(), data[indep].max(), 0.1)  # list of values to plot the regression line using
        plt.plot(x, fitted.params[1] * x + fitted.params[0], '-',
                 c='black')  # plot a line using the standard equation with parms from the model

        plt.xlabel(indep)
        plt.ylabel(dep)
        plt.savefig('{0}-{1}OLS_Sample{2}_Regression.png'.format(dep, indep, samplesize), bbox_inches='tight')
        plt.close()

