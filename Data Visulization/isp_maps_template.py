"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    gdp = {}
    with open(filename,newline="") as gdpfile:
        gdpdata= csv.DictReader(gdpfile,delimiter=separator,quotechar=quote)

        for row in gdpdata:
            rowid= row[keyfield]
            gdp[rowid]=row
    return gdp

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    plotcode_worldbankcode_dic={}
    with open(codeinfo["codefile"] ,newline="") as gdpfile:
        countrycodedata= csv.DictReader(gdpfile,delimiter=codeinfo["separator"],quotechar=codeinfo["quote"])
        for row in countrycodedata:
            plotcode_worldbankcode_dic[row[codeinfo["plot_codes"]]]=row[codeinfo["data_codes"]]
    return plotcode_worldbankcode_dic


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    plotcode_worldbankcode_dic = build_country_code_converter(codeinfo)
    print("**",plotcode_worldbankcode_dic)
    plot_not_found = set()
    mapping_dict={}
    for countrycode,countryname in plot_countries.items():
        print(countrycode)
        if countrycode.upper() in plotcode_worldbankcode_dic:
            if plotcode_worldbankcode_dic[countrycode.upper()] in gdp_countries:
                mapping_dict[countrycode]= plotcode_worldbankcode_dic[countrycode.upper()]
            else:
                plot_not_found.add(countrycode)
        #else:
         #   plot_not_found.add(countrycode)
    return mapping_dict, plot_not_found


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdpcountries = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"], gdpinfo["separator"],gdpinfo["quote"])

    plotcode_worldbankcode_dic, plot_not_found=reconcile_countries_by_code(codeinfo,plot_countries,gdpcountries)
    print("plotcode_worldbankcode_dic",plotcode_worldbankcode_dic)
    print(plot_not_found)
    gdp_notfound=set()
    plot_not_in_gdp_countries=set()
    dic_plot_to_gdp={}
    for countrycode, countryname in plot_countries.items():
        if countrycode in plotcode_worldbankcode_dic:
            if plotcode_worldbankcode_dic[countrycode] in gdpcountries:
                if gdpcountries[plotcode_worldbankcode_dic[countrycode]][year] !="":
                    dic_plot_to_gdp[countrycode]=  math.log10(float(gdpcountries[plotcode_worldbankcode_dic[countrycode]][year]))
                else:
                    gdp_notfound.add(countrycode)
            else:
                plot_not_in_gdp_countries.add(countrycode)
        else:
            plot_not_in_gdp_countries.add(countrycode)
    return dic_plot_to_gdp, plot_not_in_gdp_countries, gdp_notfound

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    return


def test_render_world_map():
    """
    Test the project code for several years
    """

    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    #print(build_country_code_converter(codeinfo))
    #gdpcountries=read_csv_as_nested_dict(gdpinfo["gdpfile"],gdpinfo["country_code"],gdpinfo["separator"],gdpinfo["quote"])
    #tups=reconcile_countries_by_code(codeinfo,pygal_countries,gdpcountries)
    #print(tups)
    #dic_plot_to_gdp, plot_not_in_gdp_countries, gdp_notfound=build_map_dict_by_code(gdpinfo,codeinfo,pygal_countries,"2010")
    dic_plot_to_gdp, plot_not_in_gdp_countries, gdp_notfound=build_map_dict_by_code({'gdpfile': 'gdptable1.csv', 'separator': ',', 'quote': '"', 'min_year': 2000, 'max_year': 2005,
         'country_name': 'Country Name', 'country_code': 'Code'}, {'codefile': 'code2.csv', 'separator': ',', 'quote': "'", 'plot_codes': 'Cd2', 'data_codes': 'Cd3'},
        {'C1': 'c1', 'C2': 'c2', 'C3': 'c3', 'C4': 'c4', 'C5': 'c5'}, '2001')
    print(dic_plot_to_gdp)
    print(plot_not_in_gdp_countries)
    print(gdp_notfound)
    # 1960
    #render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    #render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    #render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    #render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
