# MQTT/MMS Communication Logic Overview

This document outlines the bindings and communication topics used between the Server-Side and Client-Side simulation models.

## Background on Bindings

A **binding** represents a mapping between the simulation model's internal variables and the standardized communication parameters. In this architecture, it enables the integration of simulation data with the communication emulation layer. 

Key characteristics of bindings:
*   **Types of Bindings**:
    *   **Monitor Bindings**: Represent measurements, statuses, or health states. These are variables *read* from the server-side and *monitored* by the client-side.
    *   **Control Bindings**: Represent setpoints, commands, or modes. These are operations *written* by the client-side to *control* the server-side.
*   **Identification**: Each binding is uniquely identified by its **IEC 61850 Data Attribute Path** (e.g., `LD_Plant$PdCMMXU1$MX$TotW$mag$f`).
*   **Time Attribute**: Conceptually, every binding also possesses a corresponding time attribute (e.g., ending in `$t`) intended for timestamps. However, currently, *this time attribute info is not propagated through the MQTT communication*.

**CCI Assumption**: It is assumed for now that just one CCI (Controllore Centrale d'Impianto) is present, which is called `CCI_Main`. Therefore all topics use this CCI name.

## Architecture Scheme

The following diagram outlines the publish/subscribe interaction between the Simulation Models, the MQTT Broker, and the IEC 61850 MMS emulation layer.

```text
  +-------------------------+                       +-------------------------+
  |                         |                       |                         |
  |  Server-Side Sim Model  |                       |  Client-Side Sim Model  |
  |                         |                       |                         |
  +--------+---------^------+                       +--------+---------^------+
           |         |                                       |         |
  Monitor  |         | Control                      Control  |         | Monitor
  Bindings |         | Bindings                     Bindings |         | Bindings
           |         |                                       |         |
     [Pub] |         | [Sub]                           [Pub] |         | [Sub]
           v         |                                       v         |
  +--------+---------+---------------------------------------+---------+--------+
  |                                                                             |
  |                               MQTT BROKER                                   |
  |                                                                             |
  +--------+---------^---------------------------------------+---------^--------+
           |         |                                       |         |
     [Sub] |         | [Pub]                           [Sub] |         | [Pub]
           v         |                                       v         |
  +--------+---------+------+                       +--------+---------+------+
  |                         |                       |                         |
  |      IEC 61850 MMS      |                       |      IEC 61850 MMS      |
  |         SERVER          |     IEC 61850 MMS     |         CLIENT          |
  |                         | <===================> |                         |
  |  (Emulation Layer Node) |                       |  (Emulation Layer Node) |
  |                         |                       |                         |
  +-------------------------+                       +-------------------------+
```

> **Note**: There is no direct MQTT routing between the two simulation models. Instead, an emulation layer handles the communication:
> - **Monitor Bindings:** The Server-Side Sim Model publishes to MQTT. The MMS Server subscribes to these topics, forwards the updated measurements via MMS to the MMS Client, which then publishes them to MQTT for the Client-Side Sim Model to subscribe.
> - **Control Bindings:** The Client-Side Sim Model publishes control commands to MQTT. The MMS Client subscribes, forwards them via MMS to the MMS Server, which then publishes them to MQTT for the Server-Side Sim Model to execute.

---

## Server Side Simulation Topics
**CCI Name**: `CCI_Main`

### Published Topics (Monitor Bindings)
*These topics are used by the server-side sim. model to dispatch updated measurements to the client-side sim. model.*

* `CCI_Main/LD_Plant$PdCMMXU1$MX$TotW$mag$f`
  * **Description:** Read Active power measurement at the Point of Connection (PdC)
* `CCI_Main/LD_Plant$PdCMMXU1$MX$TotVAr$mag$f`
  * **Description:** Read Reactive power measurement at the Point of Connection (PdC)
* `CCI_Main/LD_Plant$VArSaDVAR1$VArTgtSptPct$mxVal$f`
  * **Description:** Read Reactive power setpoint as percentage of Smax (maximum apparent power at PdC)
* `CCI_Main/LD_Plant$VArSaDVAR1$ST$Mod$stVal`
  * **Description:** Read Function activation mode for reactive power regulation (e.g. 1=on, 5=off)
* `CCI_Main/LD_Plant$VArSaDVAR1$ST$Health$stVal`
  * **Description:** Read Physical state of the device linked to the logical node (e.g. 1=ok, 2=warning, 3=alarm)
* `CCI_Main/LD_Plant$WSaDAGC1$WSptPct$mxVal$f`
  * **Description:** Read Active power setpoint as percentage of Smax (maximum apparent power at PdC)
* `CCI_Main/LD_Plant$WSaDAGC1$ST$Mod$stVal`
  * **Description:** Read Function activation mode for active power regulation (e.g. 1=on, 5=off)
* `CCI_Main/LD_Plant$WSaDAGC1$ST$Health$stVal`
  * **Description:** Read Physical state of the device linked to the logical node (e.g. 1=ok, 2=warning, 3=alarm)

### Subscribed Topics (Control Bindings)
*These topics are used by the server-side sim. model to receive updated setpoints from the client-side sim. model.*

* `CCI_Main/LD_Plant$VArSaDVAR1$VArTgtSptPct$Oper$ctlVal$f`
  * **Description:** Write reactive power setpoint as percentage of Smax (maximum apparent power at PdC)
* `CCI_Main/LD_Plant$VArSaDVAR1$ST$Mod$Oper$ctlVal$f`
  * **Description:** Write function activation mode command for reactive power regulation (e.g. 1=on, 5=off)
* `CCI_Main/LD_Plant$WSaDAGC1$WSptPct$Oper$ctlVal$f`
  * **Description:** Write active power setpoint as percentage of Smax (maximum apparent power at PdC)
* `CCI_Main/LD_Plant$WSaDAGC1$ST$Mod$Oper$ctlVal$f`
  * **Description:** Write function activation mode command for active power regulation (e.g. 1=on, 5=off)

---

## Client Side Simulation Topics
**CCI Name**: `CCI_Main`

### Subscribed Topics (Monitor Bindings)
*These topics are used by the client-side sim. model to receive updated measurements from the server-side sim. model.*

* `cli/CCI_Main/LD_Plant$PdCMMXU1$MX$TotW$mag$f`
  * **Description:** Active power measurement at the Point of Connection (PdC)
* `cli/CCI_Main/LD_Plant$PdCMMXU1$MX$TotVAr$mag$f`
  * **Description:** Reactive power measurement at the Point of Connection (PdC)
* `cli/CCI_Main/LD_Plant$VArSaDVAR1$VArTgtSptPct$mxVal$f`
  * **Description:** Read active reactive power setpoint as percentage of Smax (maximum apparent power at PdC)
* `cli/CCI_Main/LD_Plant$VArSaDVAR1$ST$Mod$stVal`
  * **Description:** Read function activation mode for reactive power regulation (e.g. 1=on, 5=off)
* `cli/CCI_Main/LD_Plant$VArSaDVAR1$ST$Health$stVal`
  * **Description:** Read physical state of the device linked to the logical node (e.g. 1=ok, 2=warning, 3=alarm)
* `cli/CCI_Main/LD_Plant$WSaDAGC1$WSptPct$mxVal$f`
  * **Description:** Read active power setpoint as percentage of Smax (maximum apparent power at PdC)
* `cli/CCI_Main/LD_Plant$WSaDAGC1$ST$Mod$stVal`
  * **Description:** Read function activation mode for active power regulation (e.g. 1=on, 5=off)
* `cli/CCI_Main/LD_Plant$WSaDAGC1$ST$Health$stVal`
  * **Description:** Read physical state of the device linked to the logical node (e.g. 1=ok, 2=warning, 3=alarm)

### Published Topics (Control Bindings)
*These topics are used by the client-side sim. model to dispatch updated setpoints to the server-side sim. model.*

* `cli/CCI_Main/LD_Plant$VArSaDVAR1$VArTgtSptPct$Oper$ctlVal$f`
  * **Description:** Write reactive power setpoint as percentage of Smax (maximum apparent power at PdC)
* `cli/CCI_Main/LD_Plant$VArSaDVAR1$ST$Mod$Oper$ctlVal$f`
  * **Description:** Write function activation mode command for reactive power regulation (e.g. 1=on, 5=off)
* `cli/CCI_Main/LD_Plant$WSaDAGC1$WSptPct$Oper$ctlVal$f`
  * **Description:** Write active power setpoint as percentage of Smax (maximum apparent power at PdC)
* `cli/CCI_Main/LD_Plant$WSaDAGC1$ST$Mod$Oper$ctlVal$f`
  * **Description:** Write function activation mode command for active power regulation (e.g. 1=on, 5=off)
