import React from 'react';
import {AppBar,Box,Toolbar,Typography,IconButton,Menu,MenuItem,Button} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
const NavBar = () => {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const menuLinks = [
    { label: 'דף הבית', href: '/' },
    { label: 'התחברות', href: '/login' },
    { label: 'חידונים', href: '/quizzes' },
    { label: 'צור חידון', href: '/create-quiz' },
  ];

  return (
    <AppBar position="sticky">
      <Toolbar sx={{ backgroundColor: '#669999'}}>

        {/* Links for larger screens */}
        <Box variant="h2" sx={{ display: { xs: 'none', md: 'flex' }, gap: 2}}>
          {menuLinks.map((link) => (
            <Button key={link.label} color="inherit" href={link.href}>
              {link.label}
            </Button>
          ))}
        </Box>

        {/* Hamburger menu for smaller screens */}
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMenuOpen}
          >
            <MenuIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            {menuLinks.map((link) => (
              <MenuItem key={link.label} onClick={handleMenuClose}>
                <a href={link.href} style={{ textDecoration: 'none', color: 'inherit' }}>
                  {link.label}
                </a>
              </MenuItem>
            ))}
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
