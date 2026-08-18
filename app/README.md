# Project Flow (Backend)

### Authentication & Access

1. **User Registration**
2. **JWT Authentication**
3. **Role-Based Access Control**

---

### Donor

* Creates a **Donation**
* Approves a **Donation Request**

### Requester

* Requests a **Donation**

### System

* Creates a **Delivery**

### Volunteer

1. Accepts **Delivery**
2. **Picks Up** the donation
3. **Delivers** the donation

---

### Donation Lifecycle

                    ┌──────────────-┐
                    │     Donor     │
                    │Create Donation│
                    └───────┬──────-┘
                            │
                            ▼
                    ┌─────────────---┐
                    │   Requester    │
                    │Request Donation│
                    └───────┬──────--┘
                            │
                            ▼
                    ┌──────────────-┐
                    │     Donor     │
                    │Approve Request│
                    └───────┬──────-┘
                            │
                            ▼
                    ┌──────────────-┐
                    │    System     │
                    │Create Delivery│
                    └───────┬──────-┘ 
                            │
                            ▼
                    ┌──────────────-┐
                    │  Volunteer    │
                    │Accept Delivery│
                    └───────┬──────-┘
                            │
                       ┌────┴────┐
                       ▼         ▼
                    Pickup    Deliver
