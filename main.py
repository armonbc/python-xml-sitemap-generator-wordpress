from src.wpsitemapgenerator import WPXmlSitemapGenerator

if __name__ == "__main__":
   config = {
        "full_url":"https://kinsta.com/",
        "output_file":"sitemap.xml",
        "url_set_config": {
              # True = original_modification |  False = now() 
              "date_val":False,
              # True = randomize |  False = 1
              "priority_val":False,
         }
    }
   xmlgen = WPXmlSitemapGenerator(config)
   xmlgen.start()
