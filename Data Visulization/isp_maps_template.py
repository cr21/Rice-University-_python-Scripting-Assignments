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
        delimiter=codeinfo["separator"]
        quotechar=codeinfo["quote"]
        countrycodedata= csv.DictReader(gdpfile,delimiter=delimiter,quotechar=quotechar)
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
    converter = build_country_code_converter(codeinfo)
    # 'VE': 'VEN'
    converter_lower_lower={}
    for plotcode,gdpcode in converter.items():
        converter_lower_lower[plotcode.lower()]=gdpcode.lower()
    # 've': 'ven
    gdp_lower_to_original={}
    for code in gdp_countries:
        gdp_lower_to_original[code.lower()]=code
    plot_not_found = set()
    mapping_dict={}
    # 'ven': 'VEN'
    for code in plot_countries:
        if code.lower() in converter_lower_lower:
            if converter_lower_lower[code.lower()] in gdp_lower_to_original:
                mapping_dict[code]= gdp_lower_to_original[converter_lower_lower[code.lower()]]
            else:
                plot_not_found.add(code)
        else:
            plot_not_found.add(code)
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

    gdp = read_csv_as_nested_dict(gdpinfo["gdpfile"],gdpinfo["country_code"]
                                            ,gdpinfo["separator"] ,gdpinfo["quote"])

    converter=reconcile_countries_by_code(codeinfo,plot_countries,gdp)[0]
    # convert all keys and value to lower case for incase sensitive comparision
    converter_lower_lower = {}
    for plotcode, gdpcode in converter.items():
        converter_lower_lower[plotcode.lower()] = gdpcode.lower()
    # create new dictonary having keys as lowercase key of original dictonary and values having original key
    gdp_lower_to_original = {}

    for code in gdp:
        gdp_lower_to_original[code.lower()] = code

    gdp_notfound=set()
    plot_not_in_gdp_countries=set()
    dic_country_to_gdp={}

    for code in plot_countries:
        if code.lower() in converter_lower_lower:
            if converter_lower_lower[code.lower()] in gdp_lower_to_original:
                if gdp[gdp_lower_to_original[converter_lower_lower[code.lower()]]][year]!="":
                    dic_country_to_gdp[code] = math.log10(float(gdp[gdp_lower_to_original
                    [converter_lower_lower[code.lower()]]][year]))
                else:
                    #No Data for perticular year
                    gdp_notfound.add(code)
            else:
                #country not found in plotting library map data
                plot_not_in_gdp_countries.add(code)
        else:
            plot_not_in_gdp_countries.add(code)
    return dic_country_to_gdp, plot_not_in_gdp_countries, gdp_notfound

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
    dic_country_to_gdp, plot_not_in_gdp_countries, gdp_notfound = build_map_dict_by_code(gdpinfo,codeinfo,
                                                                                                    plot_countries,
                                                                                                    year)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = "GDP by country for {} (log scale),unified by common country Name ".format(year)
    worldmap_chart.add(year, dic_country_to_gdp)
    # Plot countries whose data are missing from world map
    worldmap_chart.add("Missing from World Map Data", plot_not_in_gdp_countries)
    # plot where No GDP DAta Found
    worldmap_chart.add("No GDP Data", gdp_notfound)
    # for saving in file
    # worldmap_chart.render_to_file(map_file)
    # for displaying in browser
    worldmap_chart.render_in_browser()




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

    # Example 3 plot_countries lc:UC, code _converter UC:UC, no countries in gdp_countries



    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
