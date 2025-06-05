# Task 1

Your task is to implement a React component that will generate a form based on a JSON definition. There are
only three types of fields allowed in the definition:
NumericField,
RegexValidatedField, that always comes with pattern string,
MultiSelectField, that always comes with choices values.
Consider an example definition:

```json
{
"url": "form_url",
"fields": [
{
"type": "NumericField",
"name": "number",
"label": "Number field",
"pattern": null,
"choices": null
},
{
"type": "RegexValidatedField",
"name": "string",
"label": "Only lowercase letters and underscores field",
"pattern": "[a-z_]+",
"choices": null
},
{
"type": "MultiSelectField",
"name": "selection",
"label": "Multiselect field",
"pattern": null,
"choices": [
"Choice A",
"Choice B",
"Choice C"
]
}
]
}
```

The generated form should include:
- fields as specified in the definition:
    - NumericField should only allow to input numbers,
    - RegexValidatedField should only allow strings that match provided regex pattern,
    - MultiSelectField should allow selecting multiple values from the provided choices,

- fields labels corresponding to label values,
- "submit" button that will fire a HTTP POST request to the specified url,
- "clear" button that will clear the form.

Note that there is no need to style the form. Please implement your solution starting out with this codepen:
https://codepen.io/envirly/pen/JjmQxOP