// Three.js Animated Background with Particles and Waves

let scene, camera, renderer, particles, waves;
let mouseX = 0, mouseY = 0;

function initThreeJS() {
    // Create container
    const container = document.createElement('div');
    container.id = 'threejs-background';
    document.body.insertBefore(container, document.body.firstChild);

    // Setup scene
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0f172a, 0.001);

    // Setup camera
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = 50;

    // Setup renderer
    renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Create particle system
    createParticles();

    // Create animated waves
    createWaves();

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0x6366f1, 0.5);
    scene.add(ambientLight);

    // Add point lights
    const light1 = new THREE.PointLight(0x6366f1, 1, 100);
    light1.position.set(20, 20, 20);
    scene.add(light1);

    const light2 = new THREE.PointLight(0xec4899, 1, 100);
    light2.position.set(-20, -20, -20);
    scene.add(light2);

    // Mouse move listener
    document.addEventListener('mousemove', onMouseMove, false);

    // Window resize listener
    window.addEventListener('resize', onWindowResize, false);

    // Start animation
    animate();
}

function createParticles() {
    const geometry = new THREE.BufferGeometry();
    const particleCount = 1500;
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);

    const color1 = new THREE.Color(0x6366f1);
    const color2 = new THREE.Color(0xec4899);

    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;

        // Position
        positions[i3] = (Math.random() - 0.5) * 100;
        positions[i3 + 1] = (Math.random() - 0.5) * 100;
        positions[i3 + 2] = (Math.random() - 0.5) * 100;

        // Color gradient
        const mixColor = color1.clone().lerp(color2, Math.random());
        colors[i3] = mixColor.r;
        colors[i3 + 1] = mixColor.g;
        colors[i3 + 2] = mixColor.b;

        // Size
        sizes[i] = Math.random() * 2;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const material = new THREE.PointsMaterial({
        size: 0.5,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending,
        sizeAttenuation: true
    });

    particles = new THREE.Points(geometry, material);
    scene.add(particles);
}

function createWaves() {
    const geometry = new THREE.PlaneGeometry(100, 100, 50, 50);
    const positions = geometry.attributes.position;

    // Store original positions for animation
    const originalPositions = new Float32Array(positions.count * 3);
    for (let i = 0; i < positions.count; i++) {
        originalPositions[i * 3] = positions.getX(i);
        originalPositions[i * 3 + 1] = positions.getY(i);
        originalPositions[i * 3 + 2] = positions.getZ(i);
    }
    geometry.userData.originalPositions = originalPositions;

    const material = new THREE.MeshPhongMaterial({
        color: 0x6366f1,
        wireframe: true,
        transparent: true,
        opacity: 0.15,
        side: THREE.DoubleSide
    });

    waves = new THREE.Mesh(geometry, material);
    waves.rotation.x = -Math.PI / 3;
    waves.position.z = -30;
    scene.add(waves);
}

function onMouseMove(event) {
    mouseX = (event.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);

    const time = Date.now() * 0.0005;

    // Rotate particles
    if (particles) {
        particles.rotation.y = time * 0.3;
        particles.rotation.x = time * 0.2;

        // Mouse interaction
        particles.rotation.x += mouseY * 0.05;
        particles.rotation.y += mouseX * 0.05;
    }

    // Animate waves
    if (waves) {
        const positions = waves.geometry.attributes.position;
        const originalPositions = waves.geometry.userData.originalPositions;

        for (let i = 0; i < positions.count; i++) {
            const x = originalPositions[i * 3];
            const y = originalPositions[i * 3 + 1];

            const waveX = Math.sin(x * 0.2 + time * 2) * 2;
            const waveY = Math.sin(y * 0.2 + time * 2) * 2;

            positions.setZ(i, waveX + waveY);
        }

        positions.needsUpdate = true;
        waves.rotation.z = time * 0.1;
    }

    renderer.render(scene, camera);
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThreeJS);
} else {
    initThreeJS();
}
