module.exports = {
  title: "Scarborough Dining",
  tagline: "Documentation of backend and frontend components",
  url: "https://your-docusaurus-test-site.com",
  baseUrl: "/",
  favicon: "img/favicon.ico",
  organizationName: "CSCC01", // Usually your GitHub org/user name.
  projectName: "ScarboroughDining", // Usually your repo name.
  themeConfig: {
    navbar: {
      title: "SD Docs",
      logo: {
        alt: "Logo",
        src: "img/logo.svg",
      },
      links: [
        {
          to: "docs/",
          activeBasePath: "docs",
          label: "Docs",
          position: "left",
        },
        {
          to: "docs/tests/back-tests",
          activeBasePath: "docs/tests",
          label: "Tests",
          position: "left",
        },
        {
          to: "docs/backend/backend",
          activeBasePath: "docs/backend",
          label: "Backend",
          position: "left",
        },
        {
          to: "docs/frontend/frontend",
          activeBasePath: "docs/frontend",
          label: "Frontend",
          position: "left",
        },
        {
          href: "https://github.com/CSCC01/team_08-project",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            {
              label: "Components",
              to: "docs/",
            },
          ],
        },
        {
          title: "Development",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/CSCC01/team_08-project",
            },
            {
              label: "Jira",
              href:
                "https://team-aqua.atlassian.net/secure/RapidBoard.jspa?rapidView=2",
            },
          ],
        },
        {
          title: "Community",
          items: [
            {
              label: "Live Demo",
              href: "/",
            },
            {
              label: "Website",
              href: "https://team-aqua.wixsite.com/aqua",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Team Aqua. Built with Docusaurus.`,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          // It is recommended to set document id as docs home page (`docs/` path).
          homePageId: "intro",
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl: "https://github.com/CSCC01/team_08-project",
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl: "https://github.com/CSCC01/team_08-project",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
};
