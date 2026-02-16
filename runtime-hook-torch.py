"""
Runtime hook for PyTorch to handle CUDA initialization gracefully.

This hook runs BEFORE the application starts and sets up torch
environment to gracefully handle CUDA errors in bundled executables.

It prevents torch.cuda.is_available() from crashing when CUDA DLLs
are missing or incompatible by catching and suppressing the errors.
"""

import sys
import os

# Only run in frozen (PyInstaller) mode
if getattr(sys, 'frozen', False):
    try:
        # Disable CUDA if environment variable is set
        if os.environ.get('CUDA_VISIBLE_DEVICES') is None:
            # Don't override if user explicitly set it
            # By default, we don't change anything - let torch handle it
            pass
        
        # Set environment to handle CUDA errors gracefully
        # This tells PyTorch to not fail hard if CUDA init fails
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
        
        # Import torch early to check if it's available
        try:
            import torch
            
            # Monkey-patch torch.cuda.is_available to handle errors gracefully
            _original_is_available = torch.cuda.is_available
            
            def _safe_cuda_is_available():
                """Wrapper that catches CUDA initialization errors."""
                try:
                    return _original_is_available()
                except (OSError, RuntimeError) as e:
                    # CUDA DLL initialization failed - this is expected in CPU-only builds
                    import logging
                    logging.debug(f"CUDA not available: {e}")
                    return False
                except Exception as e:
                    # Unexpected error - still return False to allow app to continue
                    import logging
                    logging.warning(f"Unexpected CUDA error: {e}")
                    return False
            
            # Replace the function
            torch.cuda.is_available = _safe_cuda_is_available
            
        except ImportError:
            # torch not available - that's fine, skip
            pass
        except OSError as e:
            # torch DLL failed to load - that's fine, application will handle it
            import logging
            logging.debug(f"PyTorch DLL initialization failed in runtime hook: {e}")
        except Exception as e:
            # Unexpected error - log but don't crash
            import logging
            logging.warning(f"Unexpected error in torch runtime hook: {e}")
            
    except Exception as e:
        # Don't let the hook crash the application
        import logging
        logging.error(f"Error in torch runtime hook: {e}")
