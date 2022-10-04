#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>
#include <functional>
#include "RungeKutta.h"
#include "Interpolation.h"

std::vector<std::vector<double>> IT = {{0.5, 6730},
                                       {1, 6790},
                                       {5, 7150},
                                       {10, 7270},
                                       {50, 8010},
                                       {200, 9185},
                                       {400, 10010},
                                       {800, 11140},
                                       {1200, 12010}};

std::vector<std::vector<double>> IM = {{0.5, 0.5},
                                       {1, 0.55},
                                       {5, 1.7},
                                       {10, 3},
                                       {50, 11},
                                       {200, 32},
                                       {400, 40},
                                       {800, 41},
                                       {1200, 39}};


std::vector<std::vector<double>> TSigma = {{4000, 0.031},
                                           {5000, 0.27},
                                           {6000, 2.05},
                                           {7000, 6.06},
                                           {8000, 12.0},
                                           {9000, 19.9},
                                           {10000, 29.6},
                                           {11000, 41.1},
                                           {12000, 54.1},
                                           {13000, 67.7},
                                           {14000, 81.5}};

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    for (auto& elem : TSigma) {
            elem[1] = std::log(elem[1]);
    }
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void calcAll(int type = 1);

const double R = 0.35;
const double l_e = 12;
const double C_k = 268 * 1e-6;
const double L_k = 187 * 1e-6;
const double R_k = 0.25;
const double U_0 = 1400;
const double I_0 = 3;
const double T_w = 2000;

double countRp(const double& I);

double integrate(double start, double emd, const std::function<double(double)> &function);

double dIdTCalc(double I, double U, double Rk, double Lk) {
    double Rp = countRp(I);
    return (U - (Rk + Rp) * I) / Lk;
}

double dIdTCalcRkRp0(double I, double U, double Rk, double Lk) {
    return (U) / Lk;
}

double dIdTCalcRkRpConst200(double I, double U, double Rk, double Lk) {
    return (U - 200 * I) / Lk;
}

double dUdTCalc(double I, double Ck) {
    return - I / Ck;
}

std::vector<double> t_vector;
std::vector<double> I_vector;
std::vector<double> U_vector;
std::vector<double> Rp_vector;
std::vector<double> ItRp_vector;
std::vector<double> T0_vector;

double tStart = 0;
double tEnd = 0.0007;
double tStep = 0.5e-6;

void calcAll(int task) {
    t_vector.clear();
    I_vector.clear();
    U_vector.clear();
    Rp_vector.clear();
    ItRp_vector.clear();
    T0_vector.clear();

    RungeKutta rungeKutta;

    double I = I_0;
    double U = U_0;
    if (task == 1) {
        for (; tStart < tEnd; tStart += tStep) {
            auto result = rungeKutta.fourth_approx(dIdTCalc, dUdTCalc, I, U, R_k, L_k, C_k, tStart, tStep);
            t_vector.push_back(tStart);
            I_vector.push_back(result[0]);
            U_vector.push_back(result[1]);
            std::cout << tStart << " " << result[0] << std::endl;
            Rp_vector.push_back(countRp(result[0]));
            ItRp_vector.push_back(result[0] * Rp_vector[Rp_vector.size() - 1]);
            T0_vector.push_back(linearInterpolate(IT, result[0]));
//            std::cout << Rp_vector[Rp_vector.size() - 1] << std::endl;
            I = result[0];
            U = result[1];
        }
    } else if (task == 2) {  // Rk + Rp = 0
        double localTEnd = tEnd * 6;
        for (; tStart < localTEnd; tStart += tStep) {
            auto result = rungeKutta.fourth_approx(dIdTCalcRkRp0, dUdTCalc, I, U, R_k, L_k, C_k, tStart, tStep);
            t_vector.push_back(tStart);
            I_vector.push_back(result[0]);
            I = result[0];
            U = result[1];
        }
    } else if (task == 3) {
        double localTEnd = 0.000020;  // 20 mcs!
//        double localTEnd = 0.0001;
        for (; tStart < localTEnd; tStart += tStep) {
            auto result = rungeKutta.fourth_approx(dIdTCalcRkRpConst200, dUdTCalc, I, U, R_k, L_k, C_k, tStart, tStep);
            t_vector.push_back(tStart);
            I_vector.push_back(result[0]);
            I = result[0];
            U = result[1];
        }
    } else if (task == 4) {

    }
}


double countRp(const double& I) {
    double T_0 = linearInterpolate(IT, I);
    double m = linearInterpolate(IM, I);

    double integral = integrate(0, 1, [&](double z) {
        double T_z = T_0 + (T_w - T_0) * pow(z, m);
        double sigma = linearInterpolate(TSigma, T_z);
        sigma = std::exp(sigma);
        return sigma * z;
    });

    double denominator = 2 * M_PI * R * R * integral;
    double res = l_e / denominator;
    return  res;
}


double integrate(double start, double emd, const std::function<double(double)> &function) {
    double h = 1e-2;
    double result = 0;

    while (start < emd) {
        double left = function(start);
        start += h;
        double right = function(start);
        result += left + right;
    }

    return result * h / 2;
}

void MainWindow::on_pushButton_clicked()
{
    calcAll();
    double a = t_vector[0];
    double b =  t_vector[t_vector.size() - 1];
    double diff = (b - a) / 8;
    a -= diff;
    b += diff;

    QVector<double> t, I, U, Rp, ItRp, T0; //Массивы координат точек
    t = t.fromStdVector(t_vector);
    I = I.fromStdVector(I_vector);
    U = U.fromStdVector(U_vector);
    Rp = Rp.fromStdVector(Rp_vector);
    ItRp = ItRp.fromStdVector(ItRp_vector);
    T0 = T0.fromStdVector(T0_vector);

    //Вычисляем наши данные

    ui->It_plot->clearGraphs();
    ui->Ut_plot->clearGraphs();
    ui->Rp_plot->clearGraphs();
    ui->ItRp_plot->clearGraphs();
    ui->T0_plot->clearGraphs();
    //Добавляем один график в widget
    ui->It_plot->addGraph();
    ui->Ut_plot->addGraph();
    ui->Rp_plot->addGraph();
    ui->ItRp_plot->addGraph();
    ui->T0_plot->addGraph();
    //Говорим, что отрисовать нужно график по нашим двум массивам x и y
    ui->It_plot->graph(0)->setData(t, I);
    ui->Ut_plot->graph(0)->setData(t, U);
    ui->Rp_plot->graph(0)->setData(t, Rp);
    ui->ItRp_plot->graph(0)->setData(t, ItRp);
    ui->T0_plot->graph(0)->setData(t, T0);

    //Подписываем оси Ox и Oy

    ui->It_plot->yAxis->setLabel("I(t)");
    ui->Ut_plot->yAxis->setLabel("U(t)");
    ui->Rp_plot->yAxis->setLabel("Rp(t)");
    ui->ItRp_plot->yAxis->setLabel("I(t) * Rp(t)");
    ui->T0_plot->yAxis->setLabel("T0(t)");


    ui->It_plot->xAxis->setLabel("t");
    ui->Ut_plot->xAxis->setLabel("t");
    ui->Rp_plot->xAxis->setLabel("t");
    ui->ItRp_plot->xAxis->setLabel("t");
    ui->T0_plot->xAxis->setLabel("t");

    //Установим область, которая будет показываться на графике
    ui->It_plot->xAxis->setRange(a, b);
    ui->Ut_plot->xAxis->setRange(a, b);
    ui->Rp_plot->xAxis->setRange(a, b);
    ui->ItRp_plot->xAxis->setRange(a, b);
    ui->T0_plot->xAxis->setRange(a, b);

    //Для показа границ по оси Oy сложнее, так как надо по правильному
    //вычислить минимальное и максимальное значение в векторах
    double It_min = *std::min_element(I_vector.begin(), I_vector.end());
    double It_max= *std::max_element(I_vector.begin(), I_vector.end());
    std::cout << "MAX IS " << It_max << std::endl;
    diff = (It_max - It_min) / 8;
    ui->It_plot->yAxis->setRange(It_min - diff,
                                 It_max + diff);


    double Ut_min = *std::min_element(U_vector.begin(), U_vector.end());
    double Ut_max= *std::max_element(U_vector.begin(), U_vector.end());
    diff = (Ut_max - Ut_min) / 8;
    ui->Ut_plot->yAxis->setRange(Ut_min - diff,
                                 Ut_max + diff);

    double Rp_min = *std::min_element(Rp_vector.begin(), Rp_vector.end());
    double Rp_max= *std::max_element(Rp_vector.begin(), Rp_vector.end());
    diff = (Rp_max - Rp_min) / 8;
    ui->Rp_plot->yAxis->setRange(Rp_min - diff,
                                 Rp_max + diff);

    double ItRp_min = *std::min_element(ItRp_vector.begin(), ItRp_vector.end());
    double ItRp_max= *std::max_element(ItRp_vector.begin(), ItRp_vector.end());
    diff = (ItRp_max - ItRp_min) / 8;
    ui->ItRp_plot->yAxis->setRange(ItRp_min - diff,
                                   ItRp_max + diff);

    double T0_min = *std::min_element(T0_vector.begin(), T0_vector.end());
    double T0_max= *std::max_element(T0_vector.begin(), T0_vector.end());
    diff = (T0_max - T0_min) / 8;
    ui->T0_plot->yAxis->setRange(T0_min - diff,
                                 T0_max + diff);


    //И перерисуем график на нашем widget
    ui->It_plot->replot();
    ui->Ut_plot->replot();
    ui->Rp_plot->replot();
    ui->ItRp_plot->replot();
    ui->T0_plot->replot();
}

void MainWindow::on_pushButton_2_clicked()
{
    calcAll(2);
    double a = t_vector[0];
    double b = t_vector[t_vector.size() - 1];
    double diff = (b - a) / 8;
    a -= diff;
    b += diff;

    QVector<double> t, I;
    t = t.fromStdVector(t_vector);
    I = I.fromStdVector(I_vector);

    //Вычисляем наши данные

    ui->RkkRp_eq0_plot->clearGraphs();
    //Добавляем один график в widget
    ui->RkkRp_eq0_plot->addGraph();
    //Говорим, что отрисовать нужно график по нашим двум массивам x и y
    ui->RkkRp_eq0_plot->graph(0)->setData(t, I);

    ui->RkkRp_eq0_plot->graph(0)->setPen(QPen(QColor(Qt::green)));

    //Подписываем оси Ox и Oy

    ui->RkkRp_eq0_plot->yAxis->setLabel("I(t)");


    ui->RkkRp_eq0_plot->xAxis->setLabel("t");

    //Установим область, которая будет показываться на графике
    ui->RkkRp_eq0_plot->xAxis->setRange(a, b);

    //Для показа границ по оси Oy сложнее, так как надо по правильному
    //вычислить минимальное и максимальное значение в векторах
    double It_min = *std::min_element(I_vector.begin(), I_vector.end());
    double It_max= *std::max_element(I_vector.begin(), I_vector.end());
    diff = (It_max - It_min) / 8;
    ui->RkkRp_eq0_plot->yAxis->setRange(It_min - diff,
                                        It_max + diff);


    //И перерисуем график на нашем widget
    ui->RkkRp_eq0_plot->replot();
}

void MainWindow::on_pushButton_3_clicked()
{
    calcAll(3);
    double a = t_vector[0];
    double b = t_vector[t_vector.size() - 1];
    double diff = (b - a) / 8;
    a -= diff;
    b += diff;

    QVector<double> t, I;
    t = t.fromStdVector(t_vector);
    I = I.fromStdVector(I_vector);

    //Вычисляем наши данные

    ui->RkkRp_const200_plot->clearGraphs();
    //Добавляем один график в widget
    ui->RkkRp_const200_plot->addGraph();
    //Говорим, что отрисовать нужно график по нашим двум массивам x и y
    ui->RkkRp_const200_plot->graph(0)->setData(t, I);

    //Подписываем оси Ox и Oy

    ui->RkkRp_const200_plot->yAxis->setLabel("I(t)");

    ui->RkkRp_const200_plot->graph(0)->setPen(QPen(QColor(Qt::red)));

    ui->RkkRp_const200_plot->xAxis->setLabel("t");

    //Установим область, которая будет показываться на графике
    ui->RkkRp_const200_plot->xAxis->setRange(a, b);

    //Для показа границ по оси Oy сложнее, так как надо по правильному
    //вычислить минимальное и максимальное значение в векторах
    double It_min = *std::min_element(I_vector.begin(), I_vector.end());
    double It_max= *std::max_element(I_vector.begin(), I_vector.end());
    diff = (It_max - It_min) / 8;
    ui->RkkRp_const200_plot->yAxis->setRange(It_min - diff,
                                             It_max + diff);


    //И перерисуем график на нашем widget
    ui->RkkRp_const200_plot->replot();
}
