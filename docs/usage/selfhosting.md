|Contents
--- |
|[Using Docker](#using-docker-recommended)
|[Python script](#python-script)

# Using Docker (recommended)
https://hub.docker.com/r/wupasscat/continentbot

|Contents
--- |
|[Docker run](#docker-run)
|[Docker compose](#docker-compose)
|[Unraid](#unraid)

## Docker run
### Prerequisites:
- Docker ([install guide](https://docs.docker.com/engine/install/))
- Discord application with bot ([create one here](https://discord.com/developers/applications))
```{code-block} bash
docker run -d --name continent-bot \
    -e DISCORD_TOKEN=discord bot token \
    -e CENSUS_API_KEY=s:example \
    -e LOG_LEVEL=INFO \
    wupasscat/continentbot:latest
```
### Environment Variables:
- `DISCORD_TOKEN` found in the "Bot" section of your Discord application
- `CENSUS_API_KEY` Daybreak Games Census API service ID  
    ```{warning}
    You can use the default value `s:example` for testing but you will be limited to 10 requests per minute.  
    It is recommended that you apply for a service ID [here](https://census.daybreakgames.com/#devSignup)

<br />

***

<br />

## Docker compose
### Prerequisites:
- Docker ([install guide](https://docs.docker.com/engine/install/))
- Docker compose ([install guide](https://docs.docker.com/compose/install/))
- Discord application with bot ([create one here](https://discord.com/developers/applications))  

From [docker-compose.yml](https://github.com/wupasscat/continent-bot/blob/main/docker-compose.yml):
```{code-block} docker
version: '3.4'
services:
    continentbot:
        container_name: continent-bot
        environment:
            - DISCORD_TOKEN=discord bot token
            - CENSUS_API_KEY=s:example
            - LOG_LEVEL=INFO
        image: 'wupasscat/continentbot:latest'
```
### Environment Variables:
- `DISCORD_TOKEN` found in the "Bot" section of your Discord application
- `CENSUS_API_KEY` Daybreak Games Census API service ID  
    ```{warning}
    You can use the default value `s:example` for testing but you will be limited to 10 requests per minute.  
    It is recommended that you apply for a service ID [here](https://census.daybreakgames.com/#devSignup)


<br />

***

<br />

## Unraid
[Template support thread](https://forums.unraid.net/topic/135184-support-wupasscats-template-repository)
### Prerequisites:
- Unraid Community Apps (CA) plugin ([install guide](https://forums.unraid.net/topic/38582-plug-in-community-applications/))

### Setup:
1. Search for `ps2-continent-bot` in the "Apps" tab of your Unraid dashboard

![unraid.png](https://raw.githubusercontent.com/wupasscat/continent-bot/main/assets/unraid.png)

### Environment Variables:
- "Discord Bot Token" found in the "Bot" section of your Discord application
- "PlanetSide 2 API service ID" Daybreak Games Census API service ID  
    ```{warning}
    You can use the default value `s:example` for testing but you will be limited to 10 requests per minute.  
    It is recommended that you apply for a service ID [here](https://census.daybreakgames.com/#devSignup)


<br />

***

<br />

# Python script

|Contents
--- |
|[Linux](#linux)

## Linux

### Prerequisites:
- `git`
- `python3`
- `python3-pip`
- Discord application with bot ([create one here](https://discord.com/developers/applications))

### Setup:
1. Clone the repository  
    ```bash
    git clone https://github.com/wupasscat/continent-bot.git
    cd continent-bot
    ```
2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Create `.env` file
    ```bash
    nano .env
    ```
    Your file should look like this:
    ```{code-block} python
    # .env
    DISCORD_TOKEN=your discord bot token
    API_KEY=s:example
    LOG_LEVEL=INFO
    ```
    - `DISCORD_TOKEN` found in the "Bot" section of your Discord application
    - `API_KEY` Daybreak Games Census API service ID  
    ```{warning}
    You can use the default value `s:example` for testing but you will be limited to 10 requests per minute.  
    It is recommended that you apply for a service ID [here](https://census.daybreakgames.com/#devSignup)

    
4. Run script
    ```bash
    python3 -m bot.py
    ```
