#include "Interpolation.h"

double linearInterpolate(std::vector<std::vector<double>>& table, double parameter) {
    size_t index = 0;
    for (; index < table.size() - 1; index++) {
        if ((parameter >= table[index][0] && parameter <= table[index + 1][0]) ||
            (parameter < table[index][0])) { break; }
    }
    if (index == table.size() - 1) {index -= 1;}

    return table[index][1] +
                 (table[index + 1][1] - table[index][1]) * (parameter - table[index][0]) /
                 (table[index + 1][0] - table[index][0]);
}