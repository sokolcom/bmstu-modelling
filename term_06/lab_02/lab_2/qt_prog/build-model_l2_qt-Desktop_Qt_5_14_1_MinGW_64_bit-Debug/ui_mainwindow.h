/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.14.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>
#include "qcustomplot.h"

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QPushButton *pushButton;
    QWidget *gridLayoutWidget;
    QGridLayout *gridLayout;
    QCustomPlot *ItRp_plot;
    QCustomPlot *Rp_plot;
    QCustomPlot *It_plot;
    QCustomPlot *T0_plot;
    QCustomPlot *Ut_plot;
    QCustomPlot *RkkRp_eq0_plot;
    QPushButton *pushButton_2;
    QCustomPlot *RkkRp_const200_plot;
    QPushButton *pushButton_3;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1077, 793);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        pushButton = new QPushButton(centralwidget);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(410, 350, 151, 91));
        gridLayoutWidget = new QWidget(centralwidget);
        gridLayoutWidget->setObjectName(QString::fromUtf8("gridLayoutWidget"));
        gridLayoutWidget->setGeometry(QRect(20, 20, 991, 321));
        gridLayout = new QGridLayout(gridLayoutWidget);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        gridLayout->setContentsMargins(0, 0, 0, 0);
        ItRp_plot = new QCustomPlot(gridLayoutWidget);
        ItRp_plot->setObjectName(QString::fromUtf8("ItRp_plot"));

        gridLayout->addWidget(ItRp_plot, 2, 1, 1, 1);

        Rp_plot = new QCustomPlot(gridLayoutWidget);
        Rp_plot->setObjectName(QString::fromUtf8("Rp_plot"));

        gridLayout->addWidget(Rp_plot, 1, 1, 1, 1);

        It_plot = new QCustomPlot(gridLayoutWidget);
        It_plot->setObjectName(QString::fromUtf8("It_plot"));

        gridLayout->addWidget(It_plot, 1, 0, 1, 1);

        T0_plot = new QCustomPlot(gridLayoutWidget);
        T0_plot->setObjectName(QString::fromUtf8("T0_plot"));

        gridLayout->addWidget(T0_plot, 1, 2, 1, 1);

        Ut_plot = new QCustomPlot(gridLayoutWidget);
        Ut_plot->setObjectName(QString::fromUtf8("Ut_plot"));

        gridLayout->addWidget(Ut_plot, 2, 0, 1, 1);

        RkkRp_eq0_plot = new QCustomPlot(centralwidget);
        RkkRp_eq0_plot->setObjectName(QString::fromUtf8("RkkRp_eq0_plot"));
        RkkRp_eq0_plot->setGeometry(QRect(20, 470, 441, 161));
        pushButton_2 = new QPushButton(centralwidget);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));
        pushButton_2->setGeometry(QRect(160, 640, 151, 91));
        RkkRp_const200_plot = new QCustomPlot(centralwidget);
        RkkRp_const200_plot->setObjectName(QString::fromUtf8("RkkRp_const200_plot"));
        RkkRp_const200_plot->setGeometry(QRect(560, 470, 441, 161));
        pushButton_3 = new QPushButton(centralwidget);
        pushButton_3->setObjectName(QString::fromUtf8("pushButton_3"));
        pushButton_3->setGeometry(QRect(690, 640, 151, 91));
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 1077, 25));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        pushButton->setText(QCoreApplication::translate("MainWindow", "TASK 1", nullptr));
        pushButton_2->setText(QCoreApplication::translate("MainWindow", "TASK 2", nullptr));
        pushButton_3->setText(QCoreApplication::translate("MainWindow", "TASK 3", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
