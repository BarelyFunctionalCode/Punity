`brain.py` will ingest and analyze user activity and then generate the context around what the user is doing to give useful responses.

THIS IS NOT MALWARE I SWEAR

## Input Types

- Keyboard Input
  - Keyboard presses are logged by Punity's environment, and is logically broke up into "logs" that try to capture full strings of data for unique application windows and timeframes.

- Mouse Click Input
  - Probably not super useful -- would only indicate that you are clicking on a certain window.

- Mouse Move Input
  - Able to aid in determining if the user is active on the computer.

## Brain Data Structure

``` python
{
  "app_pid": {
    "app_name": "whatevertheappnameis",
    "app_title": "namewithabitmorecontext", # This usually tells what specific thing you're interacting with in an application
    "raw_text_data": [
      {
        "timestamp": "sometimegoeshere",
        "text": "uhhhhhhh"
      },
    ],
    "clicks": 0, # However many times the application was clicked on
    "last_active_time": "sometimegoeshere", # Calculated by the last keyboard/mouse input for when this app was the active app
    "activity_time": 0
    "insight": "Some kind of analysis is done on the raw input data paired with the application metadata to try and piece together what the user is doing in the application. This can then preface any kind of ML queries along with the raw inputs."
  }
}
```

## Workflow

1. Brain gets input from the environment.
2. Brain organizes inputs into the data structure.
3. At certain thresholds (something that determines the brain has enough info to make some kind of response to the user), the brain will assess any new inputs and determine if it's worth querying ML model for a response.
4. Brain uses API call to query locally hosted ML model and waits for response.
5. Depending on response from ML model, brain will generate some kind of visual (text output, effect, expression).