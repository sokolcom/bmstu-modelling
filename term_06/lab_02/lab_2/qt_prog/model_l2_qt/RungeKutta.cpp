#include "RungeKutta.h"

std::vector<double> RungeKutta::fourth_approx(std::function<double(double, double, double, double)> dICalc,
                                 std::function<double(double, double)> dUCalc,
                                 double I, double U, double R_k, double L_k, double C_k, double t0, double h) {

    double k1 = h * dICalc(I, U, R_k, L_k);
    double m1 = h * dUCalc(I, C_k);

//    double k2 = h * f(x_n + h / 2, y_n + k1 / 2);
    double k2 = h * dICalc(I + k1 / 2, U + m1 / 2, R_k, L_k);
    double m2 = h * dUCalc(I + k1 / 2, C_k);

//    double k3 = h * f(x_n + h / 2, y_n + k2 / 2);
    double k3 = h * dICalc(I + k2 / 2, U + m2 / 2, R_k, L_k);
    double m3 = h * dUCalc(I + k2 / 2, C_k);


//    double k4 = h * f(x_n + h, y_n + k3);
    double k4 = h * dICalc(I + k3, U + m3, R_k, L_k);
    double m4 = h * dUCalc(I + k3, C_k);


    double newI = I + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    double newU = U + (m1 + 2 * m2 + 2 * m3 + m4) / 6;

    return {newI, newU};
}
