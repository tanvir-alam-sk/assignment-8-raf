# Trip Crawler

This project is designed for web scraping and managing data using Docker containers. It includes services for a PostgreSQL database, a web scraper, pgAdmin, and a testing setup.

## Setup Instructions

0. Make sure you have the correct environment variables set in the `.env` and `config.py` files.

   ```bash
   # config.py
   DB_USERNAME='tanvir'
   DB_PASSWORD='tanvir1234'
   DB_NAME='scrapingdb1'
   DB_PORT='5432'
   DB_HOST='postgres'

   # .env
   DB_USERNAME=tanvir
   DB_PASSWORD=tanvir1234
   DB_NAME=scrapingdb1
   TEST_DB_NAME=test_db
   DB_PORT=5432
   DB_HOST=postgres
   ```
1. Clone the repository:

   ```bash
   https://github.com/tanvir-alam-sk/assignment-8-raf crawler
   cd crawler
   ```
2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows use `source .venv/Scripts/activate`
   ```
3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
4. Stop and Remove all running containers, networks, images (clean up):

   ```bash
   docker stop $(docker ps -q)                # Stops all running containers by their IDs.

   docker rm $(docker ps -aq)                # Removes all containers, whether stopped or exited.

   docker image prune                        # Remove dangling images (unused layers). Removes image layers not associated with any container.

   docker image prune -a                     # Remove all unused images (dangling and unreferenced). Deletes all unused images, including dangling and unreferenced ones.

   docker volume prune                       # Remove unused volumes. Cleans up volumes not connected to any container.

   docker network prune                      # Remove unused networks. Removes all networks not currently used by containers.

   docker system prune -a --volumes          # Remove all unused data (containers, networks, images, and volumes). Cleans up all unused containers, images, networks, and volumes.
   ```
5. Build and start the Docker containers:

   i. Build the `Scrapy`, `Postgres`, `Tests` and `Pgadmin` Docker images:

   ```bash
   docker-compose up -d --build
   ```
   `Note: Portainer will be available at https://localhost:9443`
6. Run the Scrapy spider: When we ran `docker-compose up -d --build` in the `trip_crawler` directory, it automatically started the Scrapy spider and stoped after scraping the data. To run the spider manually, you can use the following command:

   ```bash
   docker-compose run scrapy crawl tripCrawler
   ```
   Or, you can use Portainer to run the Scrapy spider by clicking on the `Containers` tab, then clicking on the `scraper_Container` container, and then clicking on the `Start` button.

   You can see the scraped data in the `hotels` table in the `scraping_db` database in `http://localhost:5050/browser/`
7. Run the tests: When we ran `docker-compose up -d --build` in the `trip_crawler` directory, it automatically started the tests and stoped after running the tests. To run the tests manually, you can use the following command:

   ```bash
   docker-compose run tests pytest --cov=trip_crawler tests/ --cov-report=html
   ```
   Or, you can use Portainer to run the tests by clicking on the `Containers` tab, then clicking on the `tests_Container` container, and then clicking on the `Start` button.

   you can see the tests in `htmlcov/index.html`
