"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
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


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    plot_values=[]
    for year in range(gdpinfo["min_year"],gdpinfo["max_year"]+1):
        if str(year) in gdpdata:
            if gdpdata[str(year)] != "":
                plot_values.append((year,float(gdpdata[str(year)])))

    # solution using list comprehension
    #plot_values= list(map(lambda year: (year,float(gdpdata[str(year)])), [year for year in range(gdpinfo["min_year"],gdpinfo["max_year"]+1)]))
    return plot_values


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    gdp_data= read_csv_as_nested_dict(gdpinfo["gdpfile"],gdpinfo["country_name"],gdpinfo["separator"],gdpinfo["quote"])
    country_xyvalues_dic = {}
    for country in country_list:
        if country in gdp_data:
            country_gdp = gdp_data[country]
            country_plot_values = build_plot_values(gdpinfo, country_gdp)
            country_xyvalues_dic[country] = country_plot_values
        else:
            country_xyvalues_dic[country]=[]
    return country_xyvalues_dic


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    countries_plot_dict= build_plot_dict(gdpinfo,country_list)
    xy_chart = pygal.XY()
    for country,year_wise_gdp in countries_plot_dict.items():
        # add (x,y) data on chart
        xy_chart.add(country,year_wise_gdp)
    # save file
    #xy_chart.render_to_file(plot_file)
    # render in browser
    xy_chart.render_in_browser()


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, ["China"],"isp_gdp_xy_china.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

test_render_xy_plot()