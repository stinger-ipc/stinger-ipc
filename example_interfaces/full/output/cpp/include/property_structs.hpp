/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/


#pragma once
#include <string>
#include "enums.hpp"
#include "structs.hpp"


struct FavoriteNumberProperty {
    int number;
    
};

struct FavoriteFoodsProperty {
    std::string drink;
    
    int slices_of_pizza;
    
    std::string breakfast;
    
};

struct LunchMenuProperty {
    Lunch monday;
    Lunch tuesday;
};
