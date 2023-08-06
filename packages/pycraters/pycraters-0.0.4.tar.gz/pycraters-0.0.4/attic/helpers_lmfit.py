import os
import sys
import math
import shelve
import numpy as np
import matplotlib.pyplot as plt

import pycraters.IO as io		# allows data extraction from files.
import lmfit as lmf
import pycraters.fits.NestedLmfit as fitter
import pycraters.fits.poly_yamamura_1D_lmfit as pyam






import pylab
def __init__():
  params = {'axes.labelsize': 10,
            'text.fontsize': 10,
            'legend.fontsize': 7,
            'legend.labelspacing':0.33,
            'xtick.labelsize': 7,
            'ytick.labelsize': 7}#,
  #         'figure.figsize': fig_size}
  pylab.rcParams.update(params)




def ensure_data(params, geom, execline, path):
  targetfile = "%s%s.moms" % (path, params.fname())
  if (os.path.isfile(targetfile) == False):
    print("No existing data found under %s. Proceeding with simulation" % (targetfile))
    sdtrimsp_run(execline, params, geom)
    sdtrimsp_get_statistics(params, geom)
  else:
    print("%s found." % (targetfile))






# -------------------------------------------------
#      find_equilibrium_concentration()
# -------------------------------------------------

def find_equilibrium_concentration(params, geom, execline, targets, path='./', funcparams=[0]):

  '''
  For a given set of parameters, this function simulates sputtering over a range of concentrations,
  and identifies that concentration at which the sputter rate is exactly equal to the supply rate;
  i.e., the steady concentration.  Identifying this concentration is necessary for estimation of
  parameters that appear in two-component systems.
  '''



  if (len(funcparams) == 3):
    alpha = funcparams[0]
    beta = funcparams[1]
    gamma = funcparams[2]
  for tt in targets:
    params.target = tt
    if (params.funcname and len(funcparams)==3):
      gm = gamma_max(tt[1][1], alpha, beta)
      if gm <= 1.0:
        gamma *= gm
      params.cfunc = lambda depth : phistar_list(depth, tt[1][1], alpha, beta, gamma)
    ensure_data(params, geom, execline, path)

  m0e_avgs = io.array_range(path, params, "target", targets, "m0e_avg")

  n=0 #find the intersection point, where the index [n] refers to the point after intersection, and at phi[n], a is less than b
  if (m0e_avgs[n][0] > m0e_avgs[n][1]):
    a = 0
    b = 1
  else:
    a = 1
    b = 0
  while (m0e_avgs[n][a] > m0e_avgs[n][b]):
    n += 1
  #currently the above logic is only necessary to set up the while loop
  #targets has form [ [["Ga", phi],["Sb", 1-phi]], etc ]
  #for a certain range of phi. We can access these values directly through
  #targets[n] --> [["Ga", phi], ["Sb", 1-phi]]
  #targets[n][0][1]

  phi0 = targets[n-1][0][1]
  phi1 = targets[n][0][1]

  equilibrium_concentration = (phi1*(m0e_avgs[n-1][a] - m0e_avgs[n-1][b]) - phi0*(m0e_avgs[n][a] - m0e_avgs[n][b])) / (m0e_avgs[n-1][a] + m0e_avgs[n][b] - m0e_avgs[n-1][b] - m0e_avgs[n][a])

  return equilibrium_concentration





#def calculate_energy_angle_phase_diagram(wrapper, params, energies, angles, fitmethod, guess, finedeg=None, path='./', curvature_effects_dk=None):
#  for ee in energies:
#    for aa in angles:
#      params.energy = ee
#      params.angle  = aa
#      wrapper.go(params)
#  for ee in energies:






# -------------------------------------------------
#      find_pattern_transitions()
# -------------------------------------------------

def find_pattern_transitions(energy, angles, finedeg, sx_values, sy_values):

  # allocate some storage
  transitions = dict()
  transitions["energy"] = energy
  transitions["angles"] = angles

  # identify the pattern *near* theta == 0
  oldangle  = finedeg[1]
  oldvector = np.array([0, sx_values[1], sy_values[1]])
  oldpattern   = np.argmin(oldvector)

  # sweep through angles
  for kk in range(2, len(finedeg)-1):

    # identify the pattern at each new angle
    newangle  = finedeg[kk]
    newvector = np.array([0, sx_values[kk], sy_values[kk]])
    newpattern   = np.argmin(newvector)

    # if pattern changes ...
    if (newpattern != oldpattern):

      # data from old pattern
      x0 = oldangle
      y0 = oldvector[oldpattern]
      z0 = oldvector[newpattern]

      # data from new pattern
      x1 = newangle
      y1 = newvector[oldpattern]
      z1 = newvector[newpattern]

      # calculate transition angle (linear approx.)
      dxstar = - (z0-y0)*(x1-x0) / ((z1-y1)-(z0-y0))
      if dxstar < 0:  print("WARNING: dxstar was found to be %f" % (dxstar))
      tangle = oldangle + dxstar
      ttype = "%s%s" % (oldpattern, newpattern)

      if ttype not in transitions:  transitions[ttype] = tangle


    # cycle pattern information
    oldangle = newangle
    oldvector = newvector
    oldpattern = newpattern

  return transitions





# -------------------------------------------------
#      plot_energy_angle_phase_diagram()
# -------------------------------------------------

def plot_energy_angle_phase_diagram(tlist):


  thefigure = plt.figure(figsize=(6.5, 4.333))
  for t in tlist:
    anglesim = t["angles"]
    energysim = t["energy"]*np.ones(len(anglesim)) 
    plt.semilogy(anglesim, energysim, 'ko', markersize=0.5)

  # set up a list of colors
  colors = dict()
  colors['01'] = 'b'
  colors['12'] = 'r'

  # set up a dictionary of descriptors
  descriptions = dict()
  descriptions['01'] = r'smooth $\to$ parallel'
  descriptions['12'] = r'parallel $\to$ perp.'
  
  # sweep through all possible transitions
  for ii in range(3):
    for jj in range(3):

      # string describing transition type
      ttype = "%s%s" % (ii,jj)

      # get all energies for which this type is present
      energies = [ t["energy"] for t in tlist if ttype in t ]

      # get the corresponding angles at which this type occurs
      angles   = [ t[ttype] for t in tlist if ttype in t ]

      # plot (WEAK IMPLEMENTATION -- does not distinguish between multiple types.
      cstring = colors[ttype] if ttype in colors else ''
      dstring = descriptions[ttype] if ttype in descriptions else ''

      plt.semilogy(angles, energies, '%ss-' % (cstring), linewidth=3, markersize=6)

  plt.xlim(0,90)
  plt.xlabel(r'angle $\theta$')
  plt.ylabel(r'energy $E$')
  #plt.legend(loc=4)
  plt.tight_layout()

  return thefigure







# --------------------------------------------------
#    fit_moments_1D()
# --------------------------------------------------


def fit_moments_1D(params, angles, fitmethod=None, fitguess=None, path='./'):

  '''
  This function takes a set of parametric dependencies and a *range of angles,*
  and fits the zeroth, first erosive, and first redistributive moments over 
  those angles to a Yamamura-modified polynomial.

  The function also stores the fits to a file at the end of the function, and
  checks for the existence of that file at the beginning of the function.  This
  allows scripts to be re-run during testing without re-calculating the fits.
  However, it may be that this function is not the best place for this 
  functionality.

  In principle different fit methods can be provided, but this is not currently
  implemented.
  '''



  # see if fit values already exist
  fname = params.fname(['target', 'beam', 'energy'])
  if os.path.isfile('%s.momfits' % (fname)):
    f = shelve.open('%s.momfits' % (fname))
    results_list = list(f['results_list'])
    f.close()
    return results_list


  # determine number of species, and number of impacts
  species = len(params.target)
  impacts = params.impacts
  finedeg = np.linspace(0,90,91)

  # configure storage for pure or mutli-species results
  extra_species = 0
  if species > 1:  extra_species = 1
  total_species = species + extra_species

  # load moment data
  m0e_avg = -np.array( io.array_range( './', params, 'angle', angles, 'evdM0_avg' ))
  m0e_std =  np.array( io.array_range( './', params, 'angle', angles, 'evdM0_std' ))
  m1e_avg = -np.array( io.array_range( './', params, 'angle', angles, 'evdM1_avg' ))
  m1e_std =  np.array( io.array_range( './', params, 'angle', angles, 'evdM1_std' ))
  m1r_avg = np.array(io.array_range( './', params, 'angle', angles, 'rddM1_avg' ))
  m1r_std = np.array(io.array_range( './', params, 'angle', angles, 'rddM1_std' ))

  # create even fit parameter
  fp_even = lmf.Parameters()
  fp_even.add("p" , value=0.25, min=0.0)
  fp_even.add("c0", value=0.00)
  fp_even.add("c2", value=0.00)
  fp_even.add("c4", value=0.00)

  # create odd fit parameter
  fp_odd  = lmf.Parameters()
  fp_odd.add("p" , value=0.25, min=0.0)
  fp_odd.add("c1", value=0.00)
  fp_odd.add("c3", value=0.00)
  fp_odd.add("c5", value=0.00)

  # greate a global fit parameter
  fp_global  = lmf.Parameters()
  fp_global.add("p", value=0.25, min=0.0)
  

  # allocate storage
  results_list = []

  # iterate through species
  for kk in range(total_species):

    # storage for returned values
    rvals = dict()
    rvals["angles"] = angles
    rvals["finedeg"] = finedeg

    # storage for nodelist
    nodelist = []

    # M0e data
    m0e_vals = np.array( [ a[kk] for a in m0e_avg ] )
    m0e_errs = np.array( [ b[kk]/np.sqrt(params.impacts) * 1.97 for b in m0e_std ] )
    rvals["m0e_dats"] = m0e_vals
    rvals["m0e_errs"] = m0e_errs
    m0e_node = fitter.FitNode( copy.deepcopy(fp_even), pyam.poly_yamamura_1D, angles, m0e_vals, m0e_errs )
    nodelist.append(m0e_node)

    # M1e data
    m1e_vals = np.array( [ a[kk][0] for a in m1e_avg ] )
    m1e_errs = np.array( [ b[kk][0]/np.sqrt(params.impacts) * 1.97 for b in m1e_std ] )
    rvals["m1e_dats"] = m1e_vals
    rvals["m1e_errs"] = m1e_errs
    m1e_node = fitter.FitNode( copy.deepcopy(fp_odd), pyam.poly_yamamura_1D, angles, m1e_vals, m1e_errs )
    nodelist.append(m1e_node)

    # M1r data
    m1r_vals = np.array( [ a[kk][0] for a in m1r_avg ] )
    m1r_errs = np.array( [ b[kk][0]/np.sqrt(params.impacts) * 1.97 for b in m1r_std ] )
    rvals["m1r_dats"] = m1r_vals
    rvals["m1r_errs"] = m1r_errs
    m1r_node = fitter.FitNode( copy.deepcopy(fp_odd), pyam.poly_yamamura_1D, angles, m1r_vals, m1r_errs )
    nodelist.append(m1r_node)

    # SuperNode and Fitting
    snode   = fitter.FitSuperNode(nodelist, fp_global)
    result  = snode.fit()
    fparams = result.params

    rvals['m0e_fit'] = m0e_node.result.params
    rvals['m1e_fit'] = m1e_node.result.params
    rvals['m1r_fit'] = m1r_node.result.params

    results_list.append(rvals)

  # populate a shelf
  fname = params.fname(['target', 'beam', 'energy'])
  f = shelve.open('%s.momfits' % (fname))
  f['results_list'] = results_list
  f.close()
  return results_list








# --------------------------------------------------
#    linked_PDE_coefficients_1D()
# --------------------------------------------------



def linked_PDE_coefficients_1D(wrapper, params, angles, finedeg, fitmethod=None, fitguess=None, path=None):

  '''
  This function calculates *flat-target* estimates of the values of the coefficients
  through second order in the linearized equation of motion.  It provides the total
  values of these coefficients, and also the contribution from each component (if
  the target is a multi-component target).  
  
  TODO:  Provide the *total* value within the zeroth entry field.
  TODO:  Modify SX and SY to take into account estimate of curvature correction.
  TODO:  Also calculate the coefficient of the first-order hx term.
  '''

  # change to the path
  if path:
    oldpath = os.getcwd()
    os.chdir( path )

  # run simulations if needed
  for aa in angles:
    params.angle = aa
    wrapper.go(params)

  # functions we will use for fitting
  fitfuncD0 = pyam.poly_yamamura
  fitfuncD1 = pyam.poly_yamamura_derivative

  # get fitted values
  results_list = fit_moments_1D(params, angles)

  # calculate PDE coefficients in 1D
  for rvals in results_list:

    rvals["finedeg"] = finedeg
    finerad = finedeg * np.pi / 180.

    # record fitted values of the functions, themselves
    rvals["m0e_vals"] = fitfuncD0(rvals["m0e_fit"], finedeg, evenopts)
    rvals["m1e_vals"] = fitfuncD0(rvals["m1e_fit"], finedeg,  oddopts)
    rvals["m1r_vals"] = fitfuncD0(rvals["m1r_fit"], finedeg,  oddopts)
    rvals["m1_vals"]  = rvals["m1e_vals"] + rvals["m1r_vals"]

    # record fitted values of the derivatives of M1
    rvals["m0ep_vals"] = fitfuncD1(rvals["m0e_fit"], finedeg, evenopts)
    rvals["m1ep_vals"] = fitfuncD1(rvals["m1e_fit"], finedeg, oddopts )
    rvals["m1rp_vals"] = fitfuncD1(rvals["m1r_fit"], finedeg, oddopts )
    rvals["m1p_vals"]  = rvals["m1ep_vals"] + rvals["m1rp_vals"]

    # construct SX, using the approximation for explicit curvature dependence
    rvals["sxe_coeffs"] =   np.cos(finerad) * rvals["m1ep_vals"] - np.sin(finerad) * rvals["m1e_vals"]
    rvals["sxr_coeffs"] =   np.cos(finerad) * rvals["m1rp_vals"] - np.sin(finerad) * rvals["m1r_vals"]
    rvals["sxc_coeffs"] = - np.cos(finerad) * rvals["m1ep_vals"] / 2.0
    rvals["sx_coeffs"]  = rvals["sxe_coeffs"] + rvals["sxr_coeffs"] + rvals["sxc_coeffs"]

    # construct SY, using the approximation for explicit curvature dependence
    rvals["sye_coeffs"] =   np.cos(finerad)**2 / np.sin(finerad) * rvals["m1e_vals"] 
    rvals["syr_coeffs"] =   np.cos(finerad)**2 / np.sin(finerad) * rvals["m1r_vals"] 
    rvals["syc_coeffs"] = - np.cos(finerad)**2 / np.sin(finerad) * rvals["m1e_vals"] / 2.0
    rvals["sy_coeffs"]  = rvals["sye_coeffs"] + rvals["syr_coeffs"] + rvals["syc_coeffs"]

  # change to the path
  if path:
    os.chdir( oldpath )

  # construct the sum dictionary
  return results_list
  





