You can rewrite the logic for `countryCallingCode` as follows:

```json
"countryCallingCode": "{{#if (endsWith (substring (jsonPath (base64 request.headers.protected-parameters decode=true) '$.customerId') 3) '0')}}''{{else}}'+1'{{/if}}"
```

### Explanation:
1. Extracts the `customerId` using `jsonPath`.
2. Decodes it from Base64 if needed.
3. Uses `substring` to extract the last three characters.
4. Checks if the extracted value ends with '0' using `endsWith`.
5. If it ends with '0', returns an empty string (`''`).
6. Otherwise, returns `+1`.

Let me know if you need further modifications!
