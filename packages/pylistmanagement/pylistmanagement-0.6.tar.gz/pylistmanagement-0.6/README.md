# pylistmanagement
This library has 3 functions with which you can manage lists or columns of dataframes.

You can impute, operate and filter.

# Installation
Use the package manager pip to install pyimage.

```python
pip install pylistmanagement

from pylistmanagement import pylistmanagement
``` 

# Usage
## **1. impute** (list1,method="_zero_")

With this function all null values are found and imputed by the selected method.


### ****Parameters****:
  - **list1** : list-like
  
      A list or a column of a dataframe 
  - **method** : {"_zero_", "_mean_", "_median_"}, default "_zero_"

    - "_zero_"
     
        - All null values are imputed by 0
        
    - "_mean_"
     
        - All null values will be imputed by the average of the list
        
    - "_median_"
     
        - All null values will be imputed by the median of the list.
      
### ****Returns****:

Returns the original imputed list

### ****Example****:

``` python
plm=pylistmanagement()
plm.impute(list1,method= "zero")
```

## **2. column_operation**(listas,method="_concat_")

This function generates a new list with the selected method from all existing lists in the list of lists.

### ****Parameters****:
  - **listas** : list-of-lists
  
      A list of lists with 2 or more lists  

  - **method** : {"_add_", "_subtract_", "_concat_"}, default "_concat_"

    - "_add_"
     
        - Add all lists
  
    - "_subtract_"
     
        - Subtracts all lists
  
    - "_concat_"
     
        - Concatenates all lists

### ****Returns****:

Returns the new created list

### ****Example****:

``` python
plm=pylistmanagement()
plm.column_operation(listas,method = "concat")
```

## **3. filtering**(dataf,list1,filter,method=="_equal_")
This function filters a dataframe according to the selected method and filter. 

### ****Parameters****:
  - **dataf** : dataframe
  
  - **list1** : _str_
  
      The name of a column of the dataframe
  - **filter** : { _str_ or _int_/_float_ }
  
      Depending on the method, _str_ inputs would not work on other method that's not "_equal_"
  - **method** :  {"_equal_", "_higher_", "_equal_higher_", "_lower_", "_equal_lower_"}, default "_equal_"

    - "_equal_" : {_str_ / _int_ / _float_}
     
        - Dataframe will be filtered by the previous selected filter
  
    - "_higher_" : {_int_ / _float_}
     
        - Dataframe will be filtered by the previous selected filter.
  
    - "_equal_higher_" : {_int_ / _float_}
     
        - Dataframe will be filtered by the previous selected filter.
  
    - "_lower_" : {_int_ / _float_}
     
        - Dataframe will be filtered by the previous selected filter.
  
    - "_equal_lower_" : {_int_ / _float_}
     
        - Dataframe will be filtered by the previous selected filter. 


### ****Returns****:
Returns the new filtered dataframe

### ****Example****:

``` python
plm=pylistmanagement()
plm.filtering(dataf,list1,filter,method = "equal")
```

# License
[MIT](https://choosealicense.com/licenses/mit/)


# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.