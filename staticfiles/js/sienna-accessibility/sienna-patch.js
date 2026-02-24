// sienna-patch.js
class AccessibilityManager {
    constructor() {
        console.log("AccessibilityManager: Patch applied.");
    }
    addLandmarks() {
        // La funcionalidad real está en sienna.min.js, pero esta clase
        // evita que adminlte.js falle al intentar llamarla.
    }
}