#ifndef PROG_RUNGEKUTTA_H
#define PROG_RUNGEKUTTA_H

#include <cmath>
#include <iostream>
#include <functional>
#include <vector>

class RungeKutta {

public:
    std::vector<double> fourth_approx(std::function<double(double, double, double, double)> dICalc,
                                                  std::function<double(double, double)> dUCalc,
                                                  double I, double U, double R_k, double L_k, double C_k,
                                                  double t0, double h);
};


#endif //PROG_RUNGEKUTTA_H
