---
title: Module's Selected Major Components
---

## Module's Selected Major Components

The following sections are the selected major components necessary for  .....

>**For each of the following sections, use <ins>one of the two styles</ins> given near the end. *REMOVE THIS NOTE***

### Power Management

(**remove this note/placeholder**: this is where your 3.3 volt switching regulator, any other needed power regulator, and power source {if applicable} **THAT WERE SELECTED**)

For more details, review the ["Appendix - Component Selection Process - Power Mangement"](https://embedded-systems-design.github.io/EGR314DataSheetTemplate/Appendix/01-Componet-Selection/Component-Selection-Process/#power-management) selection.

### Sensor

(**remove this note/placeholder**: if applicable, this is where your  **SELECTED** sensor is shown. Otherwise, remove this section.)

For more details, review the ["Appendix - Component Selection Process - Sensor"](https://embedded-systems-design.github.io/EGR314DataSheetTemplate/Appendix/01-Componet-Selection/Component-Selection-Process/#sensor) selection.

### Actuator

(**remove this note/placeholder**: if applicable, this is where your **Selected** the actuator items go, which includes both the driver and motor. Otherwise, remove this section.)

For more details, review the ["Appendix - Component Selection Process - Actuator"](https://embedded-systems-design.github.io/EGR314DataSheetTemplate/Appendix/01-Componet-Selection/Component-Selection-Process/#actuator) selection.

-----------
> Remove the following before submitting! Use them to present the selected components

### Table 1 

> This is the example found in the assignment, uses more html

<details>
    <summary>Component selection</summary>
    <div>

    <h4>External Clock Module</h4>

    <table>
        <thead>
            <tr>
                <th>Component</th>
                <th>Pros</th>
                <th>Cons</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                      <img src="\image1.png" alt="XC1259TR-ND" /><br/>
                    XC1259TR-ND surface mount crystal<br/>
                    $1/each<br/>
                    <a href="http://www.digikey.com/product-detail/en/ECS-40.3-S-5PX-TR/XC1259TR-ND/827366">link to product</a>
                </td>
                <td>
                    * Inexpensive<br/>
                    * Compatible with PSoC<br/>
                    * Meets surface mount constraint of project
                </td>
                <td>
                    * Requires external components and support circuitry for interface<br/>
                    * Needs special PCB layout.
                </td>
            </tr>
        </tbody>
    </table>

    <p><strong>Rationale:</strong> A clock oscillator is easier ....</p>

    </div>
</details>

<!-- ### Style 2

> Also acceptable, more markdown friendly

**External Clock Module**

1. XC1259TR-ND surface mount crystal

    ![](image1.png)

    * $1/each
    * [link to product](http://www.digikey.com/product-detail/en/ECS-40.3-S-5PX-TR/XC1259TR-ND/827366)

    | Pros                                      | Cons                                                             |
    | ----------------------------------------- | ---------------------------------------------------------------- |
    | Inexpensive                               | Requires external components and support circuitry for interface |
    | Compatible with PSoC                      | Needs special PCB layout.                                        |
    | Meets surface mount constraint of project |

**Rationale:** A clock oscillator is easier ... -->
