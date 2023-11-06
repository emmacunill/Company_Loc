# LocationLogic: Data-Driven Decision Making for Your Dream Business Location

say that I get the base data from a  ongo collection and from that the project is created

## Overview

This repository is a tool designed to help you find the ideal location for your company, with a focus on meeting the requirements of employees. With a bit of creativity and data-driven decision-making, you can confidently select the perfect place to set up shop. The following README will guide you through the process and decisions made using heat maps, data analysis, and a touch of creativity.

## Table of Contents

1. [Data Adquisition & Requirements](#data-adquisition-&-Requirements)
2. [Top 3 City Selection](#top-3-city-selection)
3. [City Filtering](#city-filtering)
4. [Heat Maps Analysis](#heat-maps-analysis)
5. [Airport and Transport Comparison](#airport-and-transport-comparison)
6. [Final City Selection](#final-city-selection)
7. [Choosing the Neighborhood](#choosing-the-neighborhood)
8. [Requirements for Various Categories](#requirements-for-various-categories)
9. [Final Decision](#final-decision)
10. [Conclusion](#conclusion)

## Data Adquisition & Requirements

The project is build from a preaquired Companies base collection in Mongo. 
Frome there the first exploration and decision making is done.

Also used:

- Location API
- Foursquare API
- GeoJsons
- Folium

Among others. 

**REQUIREMENTS**


- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company staff have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not too far.
- Account managers need to travel a lot.
- Everyone in the company is between 25 and 40, give them some place to go party.
- The CEO is vegan.
- If you want to make the maintenance guy happy, a basketball stadium must be around 10 Km.
- The office dog—"Dobby" needs a hairdresser every month. Ensure there's one not too far away.

## Top 3 City Selection

After MongoDB companies collection research, three cities stood out as potential candidates: **San Francisco**, **New York**, and **London**. These cities boast a thriving startup scene and have design companies in the city, making them ideal for meeting the designer's and developers needs. Happy employees, happy life. 

## City Filtering

Given that the top two choices were in the United States, I decided to explore alternative options in the U.S. market. Seattle emerged as a strong candidate due to its proximity to tech hubs and the presence of successful startups.

## Heat Maps Analysis

Heat maps were generated to visualize the density of designer requirements in each city. 

- San Francisco Heat Map

![image](https://github.com/emmacunill/Company_Loc/blob/main/images/Captura%20de%20pantalla%202023-11-05%20a%20las%2017.58.28.png?raw=true)

- New York City Heat Map

![image](https://github.com/emmacunill/Company_Loc/blob/main/images/Captura%20de%20pantalla%202023-11-05%20a%20las%2018.10.41.png?raw=true)

- Seattle Heat Map

![image](https://github.com/emmacunill/Company_Loc/blob/main/images/Captura%20de%20pantalla%202023-11-05%20a%20las%2018.15.33.png?raw=true)


This analysis played a crucial role in eliminating Seattle from consideration, as it lacked the necessary density and did not host any design companies.

While New York had a higher density of requirements in a better distribution, San Francisco offered good potential as well.

## Airport and Transport Comparison

To make a final decision between New York and San Francisco, it was considered the accessibility of airports and public transport.

San Francisco didn't have a close airport.

And the accessibility with public transport to get to the aiport, was not optimal. There were not as many possibilities.

![image](https://github.com/emmacunill/Company_Loc/blob/main/images/Captura%20de%20pantalla%202023-11-05%20a%20las%2019.23.32.png?raw=true)

Insted in New York, there were at least 3 close airports, and a huge multitude of ways to get there, from different places in the city. 

## Final City Selection

Considering the abundance of accessible airports, efficient public transport, and the density of met employees requirements, New York, specifically Manhattan, emerged as the most suitable location for your company.

## Choosing the Neighborhood

To narrow down the ideal neighborhood within Manhattan, a geojson to restrict the display of markers to the NYC borders was used. Then various categories to determine the best neighborhoods for specific needs were analyzed.

## Requirements for Various Categories

For different requirements, the following neighborhoods emerged as optimal choices:

- Vegan restaurants and Starbucks: Upper West Side, Chelsea, and Union Square.
- Night Clubs: Chelsea and the Lower East Side.
- Transportation: Chelsea and Midtown.
- Schools: Upper West Side, West Village.
- Stadiums: Chelsea.
- Dog parks: Upper West, Chelsea, and Union Square.
- Pet grooming: Upper West, Upper East, and Union Square.

## Final Decision

Based on the data, Chelsea was identified as the best neighborhood. Its proximity to Brooklyn, where a design company is located, makes it an even more appealing choice.

From that a more thorough analysis of the neighborhood was implemented.

Here the results:

![image](https://github.com/emmacunill/Company_Loc/blob/main/images/chelsea.png?raw=true)

## Conclusion

Your company's ideal location is Chelsea, specifically near the intersection of 28th Street and 7th Avenue. This area offers excellent access to Starbucks, train stations, vegan restaurants, and much more. It is close to Madison Square Park, Herald Square, and numerous Metro stations. This neighborhood is an outstanding choice, combining convenience and a thriving business environment.

