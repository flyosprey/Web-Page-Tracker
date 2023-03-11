# How to start

### 1. Clone or Download the Repository
### 2. Create and active venv:
<code>python -m venv venv</code></br>
<code>source venv/bin/activate</code>
### 3. Install requirements:
<code>pip install -r requirements.txt</code>
### 4. Create .env and .flaskenv based on .env.example and .flaskenv.example:
### 5. Run server:
<code>flask run</code>


### Swagger available by the address -> {flask_domain}/swagger-ui

<hr>

## Endpoint #1: Page Visit Registration and Data Collection
This endpoint is used for registering user visits to web pages and collecting information about these pages.

### Detail
<ul>
    <li><b>'POST /pages'</b> - Allows users to register a page visit and collect data about the page, such as the status code, title, and domain name. 
This data is then saved to an SQL Lite database.</li>
</ul>

### Input Parameter
<ul>
    <li><b>'url':</b> The URL of the web page being visited.</li>
</ul>

### Output
The endpoint returns a JSON object containing the following information:

<ul>
    <li><b>'domain_name':</b> The domain name for which the statistics are requested.</li>
    <li><b>'url':</b> The requested URL.</li>
    <li><b>'status_code':</b> The status code of the initial URL.</li>
    <li><b>'final_url':</b> The final URL if a redirect occurred, otherwise the same as the initial URL.</li>
    <li><b>'final_status_code':</b> The status code of the final URL if a redirect occurred, otherwise the same as the initial status code.</li>
    <li><b>'title':</b> The title of the web page (parsed from HTML).</li>
</ul>

## Functionality
The endpoint retrieves the status code of the initial URL and the title of the web page. 
If a redirect occurs, the endpoint retrieves the final URL and its status code.
The collected information is then stored in a SQLite database.
The endpoint returns the information about the visit as a JSON object.

<hr>


## Endpoint #2: Statistics by Domain
This endpoint is used to obtain statistics about visits to web pages by domain.

### Detail
<ul>
    <li><b>'POST /stats'</b> Allows users to retrieve statistics about a specific domain, such as the total number of visits, the number of active URLs with a status code of 200, and a list of all URLs associated with the domain.</li>
</ul>


### Input Parameter
<ul>
    <li><b>'domain_name':</b> The domain name for which the statistics are requested. (will be normalized if it is a full URL)</li>
</ul>

### Output
The endpoint returns a JSON object containing the following information:

<ul>
    <li><b>'active_page_count':</b> The total number of visits to pages on this domain with 200 status code or redirected to 200 status code.</li>
    <li><b>'total_count':</b> The total number of visits to pages on this domain.</li>
    <li><b>'url_list':</b> A list of URLs for the pages on this domain.</li>
</ul>

## Functionality
The endpoint retrieves the information about all visits to pages on the requested domain. 
It calculates the total number of visits, the number of active visits (status code of 200), and the list of URLs. 
The endpoint returns the statistics as a JSON object.

<hr>


## Additional
<ul>
    <li>The system is designed to handle large volumes of data.</li>
</ul>
