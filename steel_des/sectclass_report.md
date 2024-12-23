<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      text-align: left; /* Align text to the left */
      margin: 0;
      padding: 0;
    }
    h1, h2, h3 {
      color: #333;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }
    th, td {
      padding: 8px;
      text-align: left; /* Align table text to the left */
      border: 1px solid #ccc;
    }
    th {
      background-color: #f4f4f4;
    }
    .highlight {
      color: #d9534f; /* Red for important warnings or sections */
    }
    @media print {
      body {
        text-align: left; /* Ensure left alignment for printing */
      }
    }
  </style>
</head>


# <u>Steel Design Calculation Report</u>

## Structural Design Codes/References

The codes/references used in this report include:
1. Eurocode 1990  
2. Eurocode 1991-1-1  
3. Eurocode 1993-1-1  

## Designed Element/Member

Element/Member Name: {elem_name}

## Section Classification
### <u>Section Properties</u>

Section Size: {section}  
Yield Strength: {yield_str} N/mm<sup>2</sup>

<u>Table 1: Section Properties</u>

|**Properties**|**Values**|**Description**|
|---|---|---|
|b|data_b|Width (mm)|
|h|data_h|Height (mm)|

<div style="page-break-before: always;"></div>

### <u>Flange Classification</u>

$c_w = h - 2t_w = $ {c_w} mm
<!--if less or equal than 72eps-->  
$c_w/t_w = $ {cwtw_res} mm $<= 72\epsilon = $ {eps_72} mm
Therefore, the flange is Class 1.

<!--if more than 72eps-->
$c_w/t_w = $ {cwtw_res} mm $> 72\epsilon = $ {eps_72}  
Therefore, the flange is not Class 1.