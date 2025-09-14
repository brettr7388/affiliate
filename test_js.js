// Test the template literal syntax
const routes = [
    { label: "Test Product", image: "/test.jpg", dest_url: "/test", slug: "test" }
];

const html = routes.map(route => `
    <div>
        <img src="${route.image}" alt="${route.label}">
        <h3>${route.label}</h3>
    </div>
`).join('');

console.log(html);
