#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = 'polynomial_data_2.csv'

# Function definitions


def is_number(number):
    """
    Checks if number is float. Returns bool
    number (float)
    """
    try:
        float(number)
        return True
    except ValueError:
        return False


def function(x_variable, coefficient_variable):
    """
    Returns x^3 + coefficient * x + 7

    x_variable (float)
    coefficient_variable (float)
    """

    return x_variable**3 + coefficient_variable * x_variable + 7


def chi_squared(coefficient_variable, x_values, function_data, uncertainties):
    """ Returns chi squared after comparing function and data for a given
    coefficient

     coefficient_variable (float)
     x_values array of floats
     function_data array of floats
     errors array of floats
     """

    prediction = function(x_values, coefficient_variable)

    return np.sum(((prediction - function_data) / uncertainties)**2)


# Read in data

X_DATA = np.array([])
FUNCTION_DATA = np.array([])
UNCERTAINTY_DATA = np.array([])

INPUT_FILE = open(FILE_NAME, 'r')

for line in INPUT_FILE:

    split_up = line.split(',')

    valid = []

    for entry in split_up:
        valid.append(is_number(entry))

    if all(valid):
        X_DATA = np.append(X_DATA, float(split_up[0]))
        FUNCTION_DATA = np.append(FUNCTION_DATA, float(split_up[1]))
        UNCERTAINTY_DATA = np.append(UNCERTAINTY_DATA, float(split_up[2]))

# Plot raw data

plt.figure(0)  # Will be plotting multiple figures. Important to help Python
#                know where they start and where they end with plt.figure()
#                and plt.show().
plt.title('Raw data', fontsize=14)
plt.xlabel('x', fontsize=14)
plt.ylabel('f(x)', fontsize=14)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.errorbar(X_DATA, FUNCTION_DATA, yerr=UNCERTAINTY_DATA, fmt='o')
plt.show()

# Find best value for coefficient by trying everything

# Using Brute Force so testing all values.
# Hard to decide on range to search across using this approach.
COEFFICIENT_VALUES = np.linspace(-54, -41, 100000)

CHI_SQUARES = np.array([])

for coefficient in COEFFICIENT_VALUES:

    CHI_SQUARES = np.append(CHI_SQUARES,
                            chi_squared(coefficient, X_DATA, FUNCTION_DATA,
                                        UNCERTAINTY_DATA))

# Plot chi^2
plt.figure()
plt.title('Chi^2 against coeffienct values', fontsize=14)
plt.xlabel('Coefficient values', fontsize=14)
plt.ylabel('Chi^2', fontsize=14)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.plot(COEFFICIENT_VALUES, CHI_SQUARES)

# Select best value
FITTED_COEFFICIENT = COEFFICIENT_VALUES[np.argmin(CHI_SQUARES)]
MINIMUM_CHI_SQUARED = np.min(CHI_SQUARES)

plt.scatter(FITTED_COEFFICIENT, MINIMUM_CHI_SQUARED, s=100, label='minimum',
            c='k')
plt.legend(fontsize=14)
plt.show()

# Visually compare result with data

plt.figure()
plt.title('Data against fit', fontsize=14)
plt.xlabel('x', fontsize=14)
plt.ylabel('f(x)', fontsize=14)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
X_VALUES = np.linspace(-10, 10, 100)

plt.errorbar(X_DATA, FUNCTION_DATA, yerr=UNCERTAINTY_DATA, fmt='o',
             label='Data')
plt.plot(X_VALUES, function(X_VALUES, FITTED_COEFFICIENT), label='Fit')
plt.legend(fontsize=14)
plt.show()

# Visually show 1 & 2 sigma values

plt.title('Chi^2 against coeffienct values', fontsize=14)
plt.xlabel('Coefficient values', fontsize=14)
plt.ylabel('Chi^2', fontsize=14)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.plot(COEFFICIENT_VALUES, CHI_SQUARES)

# fitted_coefficient = coefficient_values[np.argmin(chi_squares)]
# minimum_chi_squared = chi_squares[np.argmin(chi_squares)]

plt.scatter(FITTED_COEFFICIENT, MINIMUM_CHI_SQUARED, s=100, label='minimum',
            c='k')

# 2 sigma line

plt.plot(COEFFICIENT_VALUES, np.full(len(COEFFICIENT_VALUES),
                                     MINIMUM_CHI_SQUARED + 3.841), c='grey',
         dashes=[4, 2], label=r'2 \sigma')

plt.scatter(COEFFICIENT_VALUES[np.argmin(
    np.abs(CHI_SQUARES - MINIMUM_CHI_SQUARED - 3.84))],
            MINIMUM_CHI_SQUARED + 3.84, c='b', s=100)
plt.scatter(COEFFICIENT_VALUES[np.argmin(
    np.abs(CHI_SQUARES - MINIMUM_CHI_SQUARED - 3.835))],
            MINIMUM_CHI_SQUARED + 3.84, c='b', s=100)


# 1 sigma line
plt.plot(COEFFICIENT_VALUES, np.full(len(COEFFICIENT_VALUES),
                                     MINIMUM_CHI_SQUARED + 1), c='grey',
         dashes=[1, 1], label=r'1 \sigma')

SIGMA_INDEX = np.argmin(np.abs(CHI_SQUARES - MINIMUM_CHI_SQUARED - 1))

SIGMA = np.abs(COEFFICIENT_VALUES[SIGMA_INDEX] - FITTED_COEFFICIENT)

print(SIGMA)

plt.scatter(COEFFICIENT_VALUES[np.argmin(
    np.abs(CHI_SQUARES - MINIMUM_CHI_SQUARED - 1))],
            MINIMUM_CHI_SQUARED + 1, c='b', s=100)

# Small offset, 0.005, to get point other side
plt.scatter(COEFFICIENT_VALUES[np.argmin(
    np.abs(CHI_SQUARES - MINIMUM_CHI_SQUARED - 0.995))],
            MINIMUM_CHI_SQUARED + 1, c='b', s=100)


plt.legend(fontsize=14, loc='upper right')
plt.show()

print('We find C = {0:4.2f} +/- {1:4.2f} with a reduced chi square of'
      ' {2:3.2f}.'.format(FITTED_COEFFICIENT, SIGMA,
                          MINIMUM_CHI_SQUARED / (len(X_DATA) - 1)))
