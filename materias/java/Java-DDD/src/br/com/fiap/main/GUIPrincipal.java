package br.com.fiap.main;

import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

@SuppressWarnings("serial")
public class GUIPrincipal extends JFrame {

    private Container contentPane;
    private JMenuBar mnBarra;
    private JMenu mnArquivo, mnSistema;
    private JMenuItem miSair, miAether;
    private JLabel lbLogo;
    private ImageIcon imagemLogo;

    public GUIPrincipal() {
        inicializarComponentes();
        definirEventos();
    }

    private void inicializarComponentes() {
        setTitle("Sistema AETHER");
        setBounds(0, 0, 800, 550);

        contentPane = getContentPane();
        contentPane.setLayout(null);
        contentPane.setBackground(new Color(2, 18, 38));

        imagemLogo = new ImageIcon("imagens/aether-logo-recortada.png");

        Image imagemRedimensionada = imagemLogo.getImage().getScaledInstance(450, 250, Image.SCALE_SMOOTH);

        lbLogo = new JLabel(new ImageIcon(imagemRedimensionada));
        lbLogo.setBounds(25, 145, 750, 200);

        contentPane.add(lbLogo);

        mnBarra = new JMenuBar();

        mnArquivo = new JMenu("Arquivo");
        mnSistema = new JMenu("Sistema");

        miSair = new JMenuItem("Sair");
        miAether = new JMenuItem("Analisar Ambiente");

        setJMenuBar(mnBarra);

        mnBarra.add(mnArquivo);
        mnBarra.add(mnSistema);

        mnArquivo.add(miSair);
        mnSistema.add(miAether);
    }

    private void definirEventos() {
        miSair.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.exit(0);
            }
        });

        miAether.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                GUIAether tela = new GUIAether();

                tela.setBounds(0, 0, 800, 550);

                contentPane.removeAll();
                contentPane.add(tela);
                contentPane.repaint();
                contentPane.validate();
            }
        });
    }

    public static void main(String[] args) {
        GUIPrincipal frame = new GUIPrincipal();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        Dimension tela = Toolkit.getDefaultToolkit().getScreenSize();

        frame.setLocation(
                (tela.width - frame.getSize().width) / 2,
                (tela.height - frame.getSize().height) / 2
        );

        frame.setVisible(true);
    }
}