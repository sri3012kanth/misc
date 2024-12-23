{
  "integerField": 123456789012,
  "lastNineDigits": "{{#if (gte (length (toString integerField)) 9)}}{{substring (toString integerField) 3}}{{else}}Invalid input{{/if}}"
}
