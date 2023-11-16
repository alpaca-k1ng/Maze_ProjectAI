text_surface = font.render("You win", True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        game_surface.blit(text_surface, text_rect)
        pygame.display.flip()