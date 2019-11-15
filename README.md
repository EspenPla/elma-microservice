# elma-microservice


It can be used to import  all participants.

**An example of system config**   
```
{
  "_id": "elma-system",
  "type": "system:microservice",
  "docker": {
    "image": "espenplatou/elma:test",
    "port": 5000
  },
  "verify_ssl": true
}
```

**An example of input pipe config for incremental issues import**  
   ```
   {
  "_id": "<Name of your pipe i.e youtrack-issues>",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "<name of your system>",
    "is_chronological": true,
    "supports_since": true,
    "url": "/issues"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"]
      ]
    }
  }
}
```

**An example of input pipe config to participants**  
   ```
{
  "_id": "elma-pipe",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "elma-system",
    "url": "/entries" ## Add parameter "?since=X" to just get the latest X pages
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"]
      ]
    }
  }
}
```

