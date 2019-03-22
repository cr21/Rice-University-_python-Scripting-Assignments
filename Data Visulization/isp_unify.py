"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

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


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    dic_plot_to_gdpcountry={}
    plot_not_in_gdp_countries=set()



    for countrycode,countryname in plot_countries.items():
        if countryname in gdp_countries:
            dic_plot_to_gdpcountry[countrycode]=countryname
        else:
            plot_not_in_gdp_countries.add(countrycode)
    return dic_plot_to_gdpcountry,plot_not_in_gdp_countries


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdpdict = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
    dic_plot_to_gdp = {}
    plot_not_in_gdp_countries = set()
    plot_notfound_gdp_for_year=set()
    for countrycode, countryname in plot_countries.items():
        if countryname in gdpdict:
            if gdpdict[countryname][year]!="":
                dic_plot_to_gdp[countrycode] = math.log10(float(gdpdict[countryname][year]))
            else:
                plot_notfound_gdp_for_year.add(countrycode)
        else:
            plot_not_in_gdp_countries.add(countrycode)
    return dic_plot_to_gdp, plot_not_in_gdp_countries, plot_notfound_gdp_for_year


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    dic_plot_to_gdp,plot_not_in_gdp_countries,notfound_gdp_for_year_plot = build_map_dict_by_name(gdpinfo,plot_countries,year)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = "GDP by country for {} (log scale),unified by common country Name ".format(year)
    worldmap_chart.add(year,dic_plot_to_gdp)
    # Plot countries whose data are missing from world map
    print(plot_not_in_gdp_countries)
    worldmap_chart.add("Missing from World Map Data",plot_not_in_gdp_countries)
    #plot where No GDP DAta Found
    worldmap_chart.add("No GDP Data",notfound_gdp_for_year_plot)
    # for saving in file
    #worldmap_chart.render_to_file(map_file)
    # for displaying in browser
    worldmap_chart.render_in_browser()



def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    #render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    #render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    #render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()


