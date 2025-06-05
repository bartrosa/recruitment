import React, { useState } from 'react';


const formDefinition = {
  "url": "https://jsonplaceholder.typicode.com/posts",
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
};

const NumericField = ({ name, label, value, onChange }) => {
  const handleChange = (e) => onChange(name, e.target.value);
  return (
    <div style={{ marginBottom: '10px' }}>
      <label htmlFor={name} style={{ marginRight: '5px' }}>{label}:</label>
      <input type="number" id={name} name={name} value={value} onChange={handleChange} />
    </div>
  );
};

const RegexValidatedField = ({ name, label, pattern, value, onChange }) => {
  const handleChange = (e) => onChange(name, e.target.value);
  return (
    <div style={{ marginBottom: '10px' }}>
      <label htmlFor={name} style={{ marginRight: '5px' }}>{label}:</label>
      <input
        type="text"
        id={name}
        name={name}
        value={value}
        pattern={pattern || undefined}
        onChange={handleChange}
        title={pattern ? `Required format: ${pattern}` : ''}
      />
    </div>
  );
};

const MultiSelectField = ({ name, label, choices, value, onChange }) => {
  const handleChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions).map(option => option.value);
    onChange(name, selectedOptions);
  };
  return (
    <div style={{ marginBottom: '10px' }}>
      <label htmlFor={name} style={{ marginRight: '5px' }}>{label}:</label>
      <select multiple id={name} name={name} value={value} onChange={handleChange}>
        {choices.map(choice => <option key={choice} value={choice}>{choice}</option>)}
      </select>
    </div>
  );
};

const DynamicForm = () => {
  const getInitialFormData = (fields) => {
    const initialData = {};
    fields.forEach(field => {
      initialData[field.name] = field.type === "MultiSelectField" ? [] : "";
    });
    return initialData;
  };

  const [formData, setFormData] = useState(() => getInitialFormData(formDefinition.fields));

  const handleInputChange = (name, val) => {
    setFormData(prevData => ({ ...prevData, [name]: val }));
  };

  const handleClear = () => {
    setFormData(getInitialFormData(formDefinition.fields));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Data sending:", formData);
    alert(`Data to send:\n${JSON.stringify(formData, null, 2)}\n\nURL: ${formDefinition.url}`);
    try {
      const response = await fetch(formDefinition.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        const result = await response.json();
        console.log('Success:', result);
        alert('Success!');
      } else {
        console.error('Error:', response.statusText);
        alert(`Error: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Sending error:', error);
      alert(`Sending error: ${error.message}`);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Dynamic Generated Form</h2>
      {formDefinition.fields.map(field => {
        const commonProps = {
          key: field.name,
          name: field.name,
          label: field.label,
          value: formData[field.name],
          onChange: handleInputChange,
        };
        switch (field.type) {
          case "NumericField": return <NumericField {...commonProps} />;
          case "RegexValidatedField": return <RegexValidatedField {...commonProps} pattern={field.pattern} />;
          case "MultiSelectField": return <MultiSelectField {...commonProps} choices={field.choices} />;
          default:
            console.warn(`Unknown field type: ${field.type}`);
            return <p key={field.name}>Unsupported field type: {field.type}</p>;
        }
      })}
      <div style={{ marginTop: '20px' }}>
        <button type="submit" style={{ marginRight: '10px' }}>Send</button>
        <button type="button" onClick={handleClear}>Clear</button>
      </div>
    </form>
  );
};

export default DynamicForm;