# Request Management Guide

## Overview
This guide explains how to manage maintenance requests from the Request Details page, including updating status, assigning staff, and adding notes.

## Features Implemented

### 1. Update Status
**Purpose**: Change the status of a maintenance request and add resolution notes when closing.

**How to Use**:
1. Navigate to any request's detail page
2. Click "Update Status" in the Quick Actions section
3. Select the new status from dropdown:
   - **OPEN**: Request just created, not assigned yet
   - **IN_PROGRESS**: Staff is actively working on it
   - **PENDING**: Waiting for parts, approval, or tenant access
   - **COMPLETED**: Work is finished
   - **CLOSED**: Request is archived and resolved
4. Optionally add resolution notes (recommended for COMPLETED/CLOSED status)
5. Click "Update Status" to save

**Status Workflow**:
```
OPEN → IN_PROGRESS → COMPLETED → CLOSED
  ↓         ↓            ↓
PENDING ←────────────────┘
```

**Example Use Cases**:
- Change from OPEN to IN_PROGRESS when staff starts work
- Change to PENDING if waiting for tenant to provide access
- Change to COMPLETED and add resolution notes: "Replaced leaking faucet, tested for 30 minutes"
- Change to CLOSED after tenant confirms satisfaction

---

### 2. Assign Staff
**Purpose**: Assign maintenance staff members to work on the request.

**How to Use**:
1. Click "Assign Staff" in the Quick Actions section
2. Select a staff member from the dropdown (shows name and role)
3. Optionally add assignment notes with special instructions
4. Click "Assign Staff" to save

**Features**:
- Multiple staff can be assigned to the same request
- Each assignment is tracked with timestamp
- Assignment notes are preserved for future reference
- Only active staff members are shown in the dropdown

**Example Assignment Notes**:
- "Please coordinate with tenant for access after 6 PM"
- "Bring specialized HVAC tools"
- "This is urgent - prioritize today"
- "Follow up from previous water damage inspection"

---

### 3. Add Note
**Purpose**: Add communication notes to track updates, conversations, and progress.

**How to Use**:
1. Click "Add Note" in the Quick Actions section
2. Select author type:
   - **Staff**: For maintenance team updates
   - **Tenant**: For resident feedback or requests
3. If Staff selected, choose the staff member from dropdown
4. Enter your name
5. Write the note (max 2000 characters)
6. Click "Add Note" to save

**Note Types & Examples**:

**Staff Notes**:
- "Inspected unit - found issue with water heater thermostat"
- "Ordered replacement part, ETA 3 business days"
- "Completed repair, tested all functionality"
- "Tenant not home, left card to reschedule"

**Tenant Notes**:
- "Thank you for the quick response!"
- "Issue is worse today, water now dripping constantly"
- "I'll be available Friday afternoon for access"
- "Problem resolved, everything working perfectly now"

---

## Request Details Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ ← Request Details                        [STATUS BADGE] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Main Content (Left)          │  Sidebar (Right)        │
│  ├─ Request Information       │  ├─ SLA Target          │
│  ├─ Staff Assignments         │  ├─ Location Details    │
│  └─ Communication Notes       │  └─ Quick Actions       │
│                                │     • Update Status     │
│                                │     • Assign Staff      │
│                                │     • Add Note          │
└─────────────────────────────────────────────────────────┘
```

---

## API Endpoints Used

### Update Status
```http
PUT /requests/{request_id}
Content-Type: application/json

{
  "status": "COMPLETED",
  "resolution_notes": "Fixed electrical short in bedroom outlet"
}
```

### Assign Staff
```http
POST /requests/{request_id}/assign
Content-Type: application/json

{
  "staff_id": "690d9497128045017f1a16e2",
  "notes": "Urgent - prioritize today"
}
```

### Add Note
```http
POST /requests/{request_id}/notes
Content-Type: application/json

{
  "author_type": "staff",
  "author_id": "690d9497128045017f1a16e2",
  "author_name": "John Smith",
  "body": "Completed inspection, ordering parts"
}
```

---

## Visual Indicators

### Status Colors
- **OPEN**: Blue badge
- **IN_PROGRESS**: Yellow badge
- **PENDING**: Purple badge
- **COMPLETED**: Green badge
- **CLOSED**: Gray badge

### Assignment Status
- **In Progress**: Yellow text
- **Completed**: Green text with completion timestamp

---

## Best Practices

### For Property Managers
1. **Always update status** when work state changes
2. **Add resolution notes** when closing requests for record-keeping
3. **Assign appropriate staff** based on issue type and specialties
4. **Use notes** to track progress and communication

### For Maintenance Staff
1. **Add notes** before and after each visit
2. **Update status** to IN_PROGRESS when starting work
3. **Include details** in notes (parts needed, time spent, findings)
4. **Mark COMPLETED** when work is done

### For Tenants
1. **Add notes** if the issue changes or worsens
2. **Confirm availability** for staff access in notes
3. **Provide feedback** after work is completed

---

## Workflow Example

### Complete Lifecycle of a Request

1. **Creation** (Status: OPEN)
   - Tenant reports "Water leak under kitchen sink"
   - Priority: High, SLA: 24 hours

2. **Assignment**
   - Manager assigns "Mike Johnson - Plumber"
   - Note: "Bring pipe wrench and replacement washers"

3. **Status Update** (Status: IN_PROGRESS)
   - Staff note: "Arrived on site, inspecting issue"

4. **Communication**
   - Staff note: "Found corroded pipe fitting, need to replace"
   - Staff note: "Ordered part, will return tomorrow"

5. **Status Update** (Status: PENDING)
   - Waiting for replacement part

6. **Resumed Work** (Status: IN_PROGRESS)
   - Staff note: "Part arrived, returning to complete repair"

7. **Completion** (Status: COMPLETED)
   - Resolution notes: "Replaced corroded pipe fitting and checked all connections. Tested for 30 mins - no leaks. Also tightened adjacent connections as preventive measure."
   - Staff note: "Work completed successfully"

8. **Closure** (Status: CLOSED)
   - Tenant note: "Thank you! Everything working perfectly now."
   - Manager closes request

---

## Validation Rules

### Update Status
- ✅ Status is required
- ✅ Resolution notes optional but recommended for COMPLETED/CLOSED
- ✅ Automatically sets closed_at timestamp when status changes to CLOSED/COMPLETED

### Assign Staff
- ✅ Staff ID is required
- ✅ Must select from active staff members
- ✅ Assignment notes are optional
- ✅ Prevents duplicate active assignments for same staff

### Add Note
- ✅ Author type required (staff or tenant)
- ✅ Author name required
- ✅ Note body required (max 2000 characters)
- ✅ For staff notes, staff ID must be selected
- ✅ For tenant notes, uses tenant_id from request

---

## Troubleshooting

### "Failed to update status"
- Check backend server is running on port 8000
- Verify request ID is valid
- Check browser console for detailed error

### "Failed to assign staff"
- Ensure staff member is selected
- Verify staff member exists and is active
- Check if staff is already assigned (duplicate check)

### "Failed to add note"
- Ensure all required fields are filled
- Check note length (max 2000 characters)
- Verify author information is complete

### Modal won't open
- Refresh the page
- Check browser console for JavaScript errors
- Verify frontend server is running

---

## Testing Checklist

### Update Status Feature
- [ ] Open status modal
- [ ] Change status to each option (OPEN, IN_PROGRESS, PENDING, COMPLETED, CLOSED)
- [ ] Add resolution notes
- [ ] Submit and verify status badge updates
- [ ] Verify resolution notes appear in Request Information section

### Assign Staff Feature
- [ ] Open assign modal
- [ ] Select staff member from dropdown
- [ ] Add assignment notes
- [ ] Submit and verify assignment appears in Staff Assignments section
- [ ] Try assigning multiple staff members
- [ ] Verify timestamps are correct

### Add Note Feature
- [ ] Open note modal
- [ ] Create staff note with staff member selected
- [ ] Create tenant note
- [ ] Verify both note types appear in Communication Notes section
- [ ] Test character counter (type >2000 characters)
- [ ] Verify author name and type display correctly

---

## Database Changes

When actions are performed, the following database updates occur:

### Update Status
```javascript
// MongoDB update operation
db.requests.updateOne(
  { _id: ObjectId("...") },
  { 
    $set: { 
      status: "COMPLETED",
      resolution_notes: "...",
      closed_at: new Date(),  // if status is COMPLETED/CLOSED
      updated_at: new Date()
    }
  }
)
```

### Assign Staff
```javascript
// MongoDB update operation
db.requests.updateOne(
  { _id: ObjectId("...") },
  { 
    $push: {
      assignments: {
        staff_id: "...",
        assigned_at: new Date(),
        completed_at: null,
        notes: "..."
      }
    },
    $set: { updated_at: new Date() }
  }
)
```

### Add Note
```javascript
// MongoDB update operation
db.requests.updateOne(
  { _id: ObjectId("...") },
  { 
    $push: {
      notes: {
        _id: ObjectId(),
        author_type: "staff",
        author_id: "...",
        author_name: "...",
        body: "...",
        created_at: new Date()
      }
    },
    $set: { updated_at: new Date() }
  }
)
```

---

## Success Messages

After each successful action, you'll see:
- ✅ "Status updated successfully!"
- ✅ "Staff assigned successfully!"
- ✅ "Note added successfully!"

The page automatically refreshes to show the updated data.

---

## Summary

The Request Management features provide complete control over the maintenance request lifecycle:

1. **Track Progress**: Update status as work moves through stages
2. **Coordinate Work**: Assign appropriate staff with instructions
3. **Communicate**: Add notes for transparency and record-keeping
4. **Document Resolution**: Add final notes when closing requests

All actions are tracked in the database with timestamps and update the request in real-time!
