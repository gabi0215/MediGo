import { Outlet } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
} from '@mui/material'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import LocalHospitalIcon from '@mui/icons-material/LocalHospital'

export default function Layout() {
  const navigate = useNavigate()
  const { user, clearAuth } = useAuthStore()
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  const handleLogout = () => {
    clearAuth()
    navigate('/login')
    handleClose()
  }

  const handleProfile = () => {
    navigate('/profile')
    handleClose()
  }

  return (
    <Box>
      <AppBar position="sticky">
        <Toolbar>
          <LocalHospitalIcon sx={{ mr: 1 }} />
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, cursor: 'pointer' }}
            onClick={() => navigate('/')}
          >
            메디-고
          </Typography>

          <IconButton
            size="large"
            aria-label="account"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
          >
            <Avatar
              alt={user?.full_name || '사용자'}
              src={user?.kakao_profile_image || ''}
            />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem onClick={handleProfile}>프로필</MenuItem>
            <MenuItem onClick={() => { navigate('/orders'); handleClose() }}>
              주문 내역
            </MenuItem>
            <MenuItem onClick={handleLogout}>로그아웃</MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Outlet />
      </Container>
    </Box>
  )
}

