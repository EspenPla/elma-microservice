# elma-microservice


It can be used to import  all participants to Sesam.

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


**An example of input pipe config to participants**  
   ```
{
  "_id": "elma-pipe",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "elma-system",
    "supports_since": true,    
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

