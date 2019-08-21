from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": r"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
   

def scrape_info():
    browser = init_browser()

    #url of page to be scraped
    nasa_url='https://mars.nasa.gov/news'
    browser.visit(nasa_url)
    time.sleep(1)

    #HTML object
    html=browser.html
    #parse HTML with BeautifulSoup
    soup=BeautifulSoup(html, 'html.parser')

    #Retrieve all elements that contain book information 
    news_title= soup.find('div', class_='content_title').text
    news_p=soup.find('div', class_='article_teaser_body').text


    #url of page to be scraped
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    #HTML object
    html=browser.html
    #parse HTML with BeautifulSoup
    soup=BeautifulSoup(html, 'html.parser')

    a = soup.find("footer").find("a")
    if a.has_attr('data-fancybox-href'):
        relative_url = a['data-fancybox-href']
        featured_image_url = "https://www.jpl.nasa.gov" + relative_url
    featured_image_url 
 
    #url of page to be scraped
    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # #HTML object
    html=browser.html
    
    # #parse HTML with BeautifulSoup
    soup=BeautifulSoup(html, 'html.parser')

    output=soup.find_all('p', attrs={'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})[1]
    output_new=output.contents[0]


    # URL of page to be scraped for Mars facts
    marsFacts_url="https://space-facts.com/mars/"

    #Read URL with pandas 
    tables =pd.read_html(marsFacts_url)
    df= tables[1]
    df.columns=['Dimensions', 'value']
    df.set_index('Dimensions', inplace=True)

    #Convert data to html string
    mars_table = df.to_html()
    mars_table = mars_table.replace('\n', '')

    # URL of page to be to find Mars Hemispheres images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', attrs={'class':'description'})


    # Loop through web page to find the titles
    hemispheres = []
    for result in results:
    hem = result.find('h3').text
    hemispheres.append(hem)


    # Loop throught web page to find full sized images
    link_hem = []
    for result in results:
    img = result.find('a')['href']
    
    link_hem.append('https://astrogeology.usgs.gov' + img)

    # use browser.visit in loop to go through each hem page to find image links
    hem_img_url = []
    for link in link_hem:
    browser.visit(link)
    soup = BeautifulSoup(browser.html,"html.parser")
    li = soup.find('li')
    link = li.find('a')
    href = link['href']
    hem_img_url.append(href)

    hemisphere_image_urls = []
    for i in range(len(hem_img_url)):
        hemisphere_image_urls.append({
        "title": hemispheres[i],
        "url": hem_img_url[i]
    })

    #Store data in dictionary
    mars_data = {
        'news_title': news_title,
        'news_overview': new_p,
        'featured_image': featured_image_url,
        'mars_weather': mars_weather,
        'mars_dimensions': mars_table,
        'mars_hemisphere_url': hemisphere_image_urls
    }
    print(mars_data)
    #Close the browser after scraping
    browser.quit()

    #Return results
    return mars_data